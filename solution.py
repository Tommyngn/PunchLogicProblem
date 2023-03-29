from testcases import metaData, a

def buildJobData(punchData):
    jobData = {}

    for i in punchData['jobMeta']:
        jobData[i['job']] = {'rate': i['rate'], 'benefitsRate': i['benefitsRate']}

    return jobData

def getEEPunchData(punchData, jobData):
    eePayData = {}
    for employee in punchData['employeeData']:
        employeeName = employee['employee']
        regular = float(0)
        overtime = float(0)
        doubletime = float(0)
        wagetotal = float(0)
        benefitstotal = float(0)
        currentTotalTime = float(0)
        for punch in employee['timePunch']:
            todaysJobRates = jobData[punch['job']]
            startTime = float(punch['start'][10:].replace(':', '.', 1).replace(':',''))
            endTime = float(punch['end'][10:].replace(':','.',1).replace(':',''))
            workTime = round(float(abs(startTime - endTime)), 4)

            if (currentTotalTime + workTime) <= 40:
                regular += workTime
                wagetotal += (todaysJobRates['rate'] * workTime)
                benefitstotal += (todaysJobRates['benefitsRate'] * workTime)

            elif 40 < (currentTotalTime + workTime) <= 48:
                leftoverRegularTime = float(abs(40 - regular))
                regular += leftoverRegularTime

                leftoverOverTime = float(abs(workTime - leftoverRegularTime))
                overtime += leftoverOverTime
                wagetotal += (todaysJobRates['rate'] * workTime * 1.5)
                benefitstotal += (todaysJobRates['benefitsRate'] * workTime)

            elif (currentTotalTime + workTime) > 48:
                leftoverOverTime = float(abs(8 - overtime))
                overtime += leftoverOverTime

                leftoverDoubleTime = float(abs(workTime - leftoverOverTime))
                doubletime += leftoverDoubleTime
                wagetotal += (todaysJobRates['rate'] * workTime * 2)
                benefitstotal += (todaysJobRates['benefitsRate'] * workTime)

            currentTotalTime += workTime

        eePayData[employeeName] = {
            'employee': employeeName,
            'regular': round(regular, 4),
            'overtime': round(overtime,4),
            'doubletime': round(doubletime,4),
            'wageTotal': round(wagetotal,2),
            'benefitsTotal': round(benefitstotal,2)
        }
    return eePayData



d = buildJobData(metaData)
result = getEEPunchData(metaData, d)

for i, j in result.items():
    print(j)



"""
This module generate the full informaition about all vacansies on the HH.ru
"""

def getMinSalary(salary: str):
    resultList = []
    for el in salary.split():
        if el.isdigit():
            resultList.append(el)
    if len(resultList) >= 2 and resultList[1] == '000':
        return int(resultList[0] + resultList[1])
    return int(resultList[0])

def getMaxSalary(salary: str):
    resultList = []
    for el in salary.split():
        if el.isdigit():
            resultList.append(el)
    if len(resultList) == 1:
        return int(resultList[0])
    if len(resultList) == 2 and resultList[1] == '000':
        return int(resultList[0] + resultList[1])
    if len(resultList) == 2 and resultList[1] != '000':
        return int(resultList[1])
    if len(resultList) == 3:
        return int(resultList[1] + resultList[2])
    return int(resultList[2] + resultList[3])

def getSalaryCurrency(salary: str):
    resultList = []
    for el in salary.split():
        if el.isdigit() == False:
            resultList.append(el)
    if 'бел.' in resultList:
        return resultList[-2] + resultList[-1]
    return resultList[-1]

def makeSalaryInfo(salary: str, flag):
    """Make the object with the salary info for current vacansy"""

    salary_info = {}
    if flag == 'от':
        salary_info['min_salary'] = getMinSalary(salary.text)
        salary_info['max_salary'] = None
    elif flag == 'до':
        salary_info['min_salary'] = None
        salary_info['max_salary'] = getMaxSalary(salary.text)
    elif flag == 'нет':
        salary_info['min_salary'] = getMinSalary(salary.text)
        salary_info['max_salary'] = getMaxSalary(salary.text)
    salary_info['salary_currency'] = getSalaryCurrency(salary.text)
    return salary_info


def getHeadHunterVacansies(vacansies, url):
    """Make the object of full information about all vacansies"""

    data = []
    for el in vacansies:
        v_data = {}
        v_data['vacansy_name'] = el.find('a', {'data-qa':'vacancy-serp__vacancy-title'}).text
        v_data['from'] = url
        v_data['vacansy_link'] = el.find('a', {'data-qa':'vacancy-serp__vacancy-title'}).get('href')
        vacansy_salary = el.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'})
        if vacansy_salary is not None and vacansy_salary.text[:2:] != 'от' and vacansy_salary.text[:2:] != 'до':
            v_data['salary_info'] = makeSalaryInfo(vacansy_salary, 'нет')
        elif vacansy_salary is not None and vacansy_salary.text[:2:] == 'от':
            v_data['salary_info'] = makeSalaryInfo(vacansy_salary, 'от')
        elif vacansy_salary is not None and vacansy_salary.text[:2:] == 'до':
            v_data['salary_info'] = makeSalaryInfo(vacansy_salary, 'до')
        else:
            v_data['salary_info'] = None
        data.append(v_data)
    return data


if __name__ == '__main__':
        getHeadHunterVacansies(vacansies, url)


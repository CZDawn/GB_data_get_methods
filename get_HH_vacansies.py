"""
This module generate the full informaition about all vacansies on the HH.ru
"""

def getMinSalary(salary: str):
    """Find the minimum sallary from current vacansy"""
    if len(salary.split()) < 5:
        return int(salary.split()[0])
    return int(salary.split()[0] + salary.split()[1])


def getMaxSalary(salary: str):
    """Find the maximum sallary from current vacansy"""
    if len(salary.split()) > 5:
        return int(salary.split()[-3] + salary.split()[-2])
    return int(salary.split()[-2] + salary.split()[-1])


def getSalaryCurrency(salary: str):
    """Find the currensy of sallary in current vacansy"""

    if salary.text[-4::][0] == ' ':
        return salary.text[-4::].replace(' ', '')
    return salary.text[-4:-1:]


def makeSalaryInfo(salary: str, flag):
    """Make the object with the salary info for current vacansy"""

    salary_info = {}
    if flag == 'от':
        salary_info['min_salary'] = getMinSalary(salary.text[2:-4:])
        salary_info['max_salary'] = None
    elif flag == 'до':
        salary_info['min_salary'] = None
        salary_info['max_salary'] = getMaxSalary(salary.text[2:-4:])
    elif flag == 'нет':
        salary_info['min_salary'] = getMinSalary(salary.text[:-4:])
        salary_info['max_salary'] = getMaxSalary(salary.text[:-4:])
    salary_info['salary_currency'] = getSalaryCurrency(salary)
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


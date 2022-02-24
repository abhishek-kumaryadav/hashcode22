import sys
import math
import bisect
from sys import stdin, stdout
from math import gcd, floor, sqrt, log
from collections import defaultdict as dd
from itertools import permutations
from bisect import bisect_left as bl, bisect_right as br
from functools import lru_cache

sys.setrecursionlimit(100000000)
import copy

int_r = lambda: int(sys.stdin.readline())
str_r = lambda: sys.stdin.readline().strip()
intList_r = lambda: list(map(int, sys.stdin.readline().strip().split()))
strList_r = lambda: list(sys.stdin.readline().strip())
jn = lambda x, l: x.join(map(str, l))
mul = lambda: map(int, sys.stdin.readline().strip().split())
mulf = lambda: map(float, sys.stdin.readline().strip().split())
ceil = lambda x: int(x) if (x == int(x)) else int(x) + 1
ceildiv = lambda x, d: x // d if (x % d == 0) else x // d + 1
flush = lambda: stdout.flush()
outStr = lambda x: stdout.write(str(x))
mod = 1000000007

assignment = list()
assignments = list()
projects = dict()
people = dict()
projectsO = dict()
peopleO = dict()


def main():
    global assignment
    global assignments
    global projects
    global projectsO
    global people
    global peopleO
    filename = sys.argv[1]
    with open(filename + ".txt", "rt") as f:
        nump, numpro = list(map(int, f.readline().strip().split()))
        for _ in range(nump):
            namee, numskill = list(f.readline().strip().split())
            numskill = int(numskill)
            dic = dict()
            for _t in range(numskill):
                skillname, level = list(f.readline().strip().split())
                dic[skillname] = int(level)
            people[namee] = dic
        for _ in range(numpro):
            namee, finish, score, bestBefore, roles = list(f.readline().strip().split())
            projects[namee] = list()
            roles = int(roles)
            dic = dict()
            for _t in range(roles):
                skillname, level = list(f.readline().strip().split())
                dic[skillname] = int(level)
            projects[namee].append(int(finish))
            projects[namee].append(int(score))
            projects[namee].append(int(bestBefore))
            projects[namee].append(roles)
            projects[namee].append(dic)
        # print(people, projects)
        # print(people["Anna"])
        projectsO = copy.deepcopy(projects)
        # peopleO = copy.deepcopy(people)
    answers = rePro()
    print("after rePro")
    with open(filename + "_ans.txt", "w") as f:
        f.write(str(len(answers)) + "\n")
        for ans, val in answers.items():
            proj = projectsO[ans]
            f.write(ans + "\n")
            vallist = list()
            for a, v in proj[4].items():
                for vvv in val:
                    if a == vvv[0]:
                        vallist.append(vvv[1])
            strr = " ".join(vallist)
            print(strr)
            f.write(strr)
            f.write("\n")
    print(answers)


def rePro():
    global projects, people, assignment, assignments
    answers = dict()
    length = len(projects)
    while len(projects) != 0:
        # print(projects, people)

        minBB = math.inf
        minp = ""
        assgndict = dict()
        for p in projects:
            namee = p
            finish, score, bestBefore, _, dic = projects[p]
            assignment = list()
            assignments = list()
            recurse(dic, people, p)
            print("after recurse")
            assgndict[namee] = copy.deepcopy(assignments)
            # print(assignments, bestBefore, namee)
            if len(assignments) != 0:
                if minBB > bestBefore:
                    minBB = bestBefore
                    minp = namee
            # print(minp)
        # break
        # try:
        try:
            people = increment(assgndict[minp][0], projects[minp], people)
            answers[minp] = copy.deepcopy(assgndict[minp][0])
            projects.pop(minp)
        except:
            pass
        # print(projects, people)
        print(length)
        if length == len(projects):
            break
        else:
            length -= 1
    return answers

    # break
    # except:
    # pass
    # remove from projects
    # increment


def increment(ass, p, people):
    pepe = copy.deepcopy(people)
    for a in ass:
        sub, person = a  # p[4] is dictionary
        if p[4][sub] >= people[person][sub]:
            pepe[person][sub] += 1
    return pepe


def checkMentor(ass, p):
    global people
    remaining = list()
    for a in ass:
        sub, person = a  # p[4] is dictionary
        if p[4][sub] == people[person][sub] + 1:
            remaining.append((sub, p[4][sub]))

    for a in ass:
        sub, person = a
        if p[4][sub] <= people[person][sub]:
            try:
                remaining.remove((sub, p[4][sub]))
            except:
                pass
    if len(remaining) == 0:
        return True
    else:
        return False


def recurse(req, left, pname):
    global assignment
    global assignments
    global projects
    sortedDic = dict(sorted(req.items(), key=lambda item: item[1]))
    # print(req, sortedDic)
    print("len req: ", len(req))
    if len(req) == 0:
        # if with mentoring is possible
        if checkMentor(assignment, projects[pname]):
            assignments.append(copy.deepcopy(assignment))
        # print(assignment)
        return True

    for r, l in sortedDic.items():
        minimum = dict()
        for p, s in left.items():
            if r in s.keys() and s[r] >= l - 1:
                minimum[p] = s[r]
        if len(minimum) == 0:
            return False
        minimum = dict(sorted(minimum.items(), key=lambda item: item[1]))
        for m in minimum:
            new_req = copy.deepcopy(req)
            new_req.pop(r)
            new_m = copy.deepcopy(left)
            new_m.pop(m)
            assignment.append([r, m])
            if not recurse(new_req, new_m, pname):
                return False

            # if recurse(new_req, new_m):
            # return True
            # else:
            assignment.pop()

        # req, minimum
        # iterate minimum
        # recurse(req-r, minimum-m)


if __name__ == "__main__":
    main()

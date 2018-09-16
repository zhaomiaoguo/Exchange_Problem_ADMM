from Lib import *

# sets
A = {1,2} # two agents
G = {1,2} # two goods

## parameters
beta = {} # utility coefficients beta
e = {} # endownment
x_ans = {} # quantities of goods, indexed by a, g, iter
y_ans = {} # price
x_old = {}
x_new = {}
y_old = {}
y_new = {}
x_a_ans = {} # temp solution holder for x, indexed by g
rho = {} # augment lagrangian parameter, need to increase for each iteration
err = {} # error at each iteration
eps = 1e-1 # small number for convergence check
max_iter = 2000 # maximum iteration nubmers

# utility coefficients U_a = \beta_{a1} \ln x_1 + \beta_{a2} \ln x_2
# beta indexed by A, G
beta[1, 1] = 10
beta[1, 2] = 1
beta[2, 1] = 1
beta[2, 2] = 10

# endownment indexed by A, G
e[1, 1] = 55
e[1, 2] = 0
e[2, 1] = 0
e[2, 2] = 110

# initial values

# parameters & solutions for each iterations
for iter in xrange(0,1):
    rho[iter] = 0.001
    for g in G:
       y_ans[g, iter] = 2
       for a in A:
            x_ans[a, g, iter] = 55 #  the third index is for 0 is the the initial value


time_bq={}
start = time.time()
time_bq[0] = start

for iter in xrange(1,max_iter):
    print 'Iteration #%i' % iter
    rho[iter] = 1 * rho[iter - 1]
    print 'Curent rho: %f' % rho[iter]
    # Step 1
    for g in G:
        y_old[g] = y_ans[g, iter - 1]
        for a in A:
            x_old[a, g] = x_ans[a, g, iter - 1]

    for a in A:
        x_a_ans = step_1(x_old, y_old, rho[iter], a, e, A, G, beta)
        for g in G:
            x_new[a,g] = x_a_ans[g]
            x_ans[a, g, iter] = x_new[a, g]

    # Step 2
    y_new = step_2(x_new, y_old, rho[iter], e, A, G)
    for g in G:
        y_ans[g, iter] = y_new[g]

    # check convergence
    err[iter] = sum((y_new[g] - y_old[g])**2 for g in G) + sum(sum((x_new[a,g] - x_old[a,g])**2 for g in G ) for a in A) + sum( sum((x_new[a, g] - e[a, g]) for a in A)**2 for g in G)
    print 'curent gap: %f' % err[iter]
    if err[iter] < eps:
        break
#
end = time.time()
el_time = end - start

print 'Total Computing Time: %f' % el_time

#print solutions
group = 0
cdict = {1:'b', 2: 'g', 3:'r', 4: 'c', 5: 'm', 6: 'y', 7:'k', 8:'w'}
for a in A:
    for g in G:
        group = group + 1
        for iter in xrange(0, max([key[2] for key in x_ans.keys()])):

            plt.scatter(iter, x_ans[a, g, iter], c = cdict[group], s = 10)

plt.show()

# print error
print_dict(err)
plt.show()

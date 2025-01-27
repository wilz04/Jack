# IC 6101 1er Semestre 2017
# Nombre: Wilberth Castro
# Correo: wilz04@gmail.com

# En la politica, el numero de fila representa la cantidad de autos en el local 1,
# el numero de columna representa la cantidad de autos en el local 2
# y valor en la celda representa la accion (cantidad de autos desplazados de 1 a 2)

from math import exp


ncar_states = 21
max_moves = 5
max_morning = ncar_states + max_moves # 26
discount = 0.9
theta = 1*10**-7


prob_1 = [[.0]*ncar_states for i in range(0, max_morning)]
prob_2 = [[.0]*ncar_states for i in range(0, max_morning)]

rew_1 = [.0]*max_morning
rew_2 = [.0]*max_morning

V = [[.0]*ncar_states for i in range(ncar_states)]
policy = [[0]*ncar_states for i in range(ncar_states)]


def factorial(n):
	if n > 0:
		return n*factorial(n-1)
	else:
		return 1.0

def poisson(n, lmbda):
	return (exp(-lmbda)*lmbda**n)/factorial(n)

def load_probs_rewards(probs, rewards, l_reqsts, l_drpffs):
	req_prob = 1.0
	drp_prob = 1.0
	satisfied_req = .0
	new_n = .0
	
	# print "loading.."
	
	req = 0
	while req_prob > theta:
		req_prob = poisson(req, l_reqsts)
		# print "req: " + str(req) + ", req_prob: " + str(req_prob) + ", "
		
		for n in range(0, max_morning):
			satisfied_req = min(req, n)
			rewards[n] += 10*req_prob*satisfied_req
			# print "satisfied_req: " + str(satisfied_req) + ", reward: " + str(10*req_prob*satisfied_req) + ", "
		
		drp = 0
		while drp_prob > theta:
			drp_prob = poisson(drp, l_drpffs)
			
			for m in range(0, max_morning):
				satisfied_req = min(req, m)
				new_n = m + drp - satisfied_req
				new_n = max(new_n, 0)
				new_n = min(20, new_n)
				probs[m][new_n] += req_prob*drp_prob
			
			drp += 1
		
		req += 1

def policy_eval():
	val_tmp = .0
	diff = 1.0
	a = 0
	while diff > theta:
		diff = .0
		for n1 in range(0, ncar_states):
			for n2 in range(0, ncar_states):
				val_tmp = V[n1][n2]
				a = policy[n1][n2]
				V[n1][n2] = backup_action(n1, n2, a)
				diff = max(diff, abs(V[n1][n2] - val_tmp))

def backup_action(n1, n2, a, trace=False):
	a = min(a, +n1)
	a = max(a, -n2)
	a = min(+5, a)
	a = max(-5, a)
	val = -2*abs(a)
	buffer = str(-2*abs(a))
	morning_n1 = n1 - a
	morning_n2 = n2 + a
	for new_n1 in range(0, ncar_states):
		for new_n2 in range(0, ncar_states):
			val += prob_1[morning_n1][new_n1]*prob_2[morning_n2][new_n2] * (rew_1[morning_n1] + rew_2[morning_n2] + discount*V[new_n1][new_n2])
			buffer += "; " + str(prob_1[morning_n1][new_n1]*prob_2[morning_n2][new_n2] * (rew_1[morning_n1] + rew_2[morning_n2] + discount*V[new_n1][new_n2]))
	if trace:
		file = open("trace.txt", "a")
		file.write(buffer + "\n")
		file.close()
		# print buffer + "<br />"
	return val

def update_policy_t():
	b = 0
	has_changed = False
	for n1 in range(0, ncar_states):
		for n2 in range(0, ncar_states):
			b = policy[n1][n2]
			policy[n1][n2] = greedy_policy(n1, n2)
			if b != policy[n1][n2]:
				has_changed = True
	return has_changed

def greedy_policy(n1, n2):
	a_min = max(-5, -n2)
	a_max = min(+5, +n1)
	best_val = backup_action(n1, n2, a_min)
	best_action = a_min
	for a in range(a_min + 1, a_max + 1):
		val = backup_action(n1, n2, a)
		# print val
		# print a
		if val > best_val + 1*10**-9:
			best_val = val
			best_action = a
	# print best_action
	# print "----"
	return best_action

def print_policy():
	buffer = ""
	for n1 in range(0, ncar_states):
		for n2 in range(0, ncar_states):
			buffer += str(policy[ncar_states - (n1 + 1)][n2]) + "; "
		
		buffer += "\n"
	
	print buffer;

def print_rew(rew):
	buffer = ""
	for n1 in range(0, max_morning):
		buffer += "\t" + str(rew[n1]) + "; "
	
	print buffer;

def print_prob(prob):
	buffer = ""
	for n1 in range(0, max_morning):
		for n2 in range(0, ncar_states):
			buffer += "\t" + str(prob[n1][n2]) + "; "
		
		buffer += "<br />"
	
	print buffer;

def print_v():
	buffer = ""
	for n1 in range(0, ncar_states):
		for n2 in range(0, ncar_states):
			buffer += "\t" + str(V[n1][n2]) + "; "
		
		buffer += "<br />"
	
	print buffer;

def main():
	lmbda_1r = 3.0
	lmbda_1d = 3.0
	lmbda_2r = 4.0
	lmbda_2d = 2.0
	
	load_probs_rewards(prob_1, rew_1, lmbda_1r, lmbda_1d)
	load_probs_rewards(prob_2, rew_2, lmbda_2r, lmbda_2d)
	
	# print_rew(rew_1)
	# print_rew(rew_2)
	# print_prob(prob_1)
	# print_prob(prob_2)
	
	has_changed = True
	while has_changed:
		policy_eval();
		# print_v()
		has_changed = update_policy_t();
	
	print_policy();

main()

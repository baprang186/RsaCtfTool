import os
import subprocess
import re

class SiqsAttack:
    def __init__(self, args, n):
        # Configuration
        self.yafubin = "./yafu"  # where the binary is
        self.threads = 2        # number of threads
        self.maxtime = 180      # max time to try the sieve

        self.n = n
        self.p = None
        self.q = None
        self.verbose = args.verbose

    def testyafu(self):
        with open(os.devnull, 'w') as DN:
            try:
                yafutest = subprocess.check_output(
                    [self.yafubin, 'siqs(1549388302999519)'], stderr=DN
                ).decode('utf-8')
            except subprocess.CalledProcessError:
                yafutest = ""

        if '48670331' in yafutest:
            # yafu is working
            if self.verbose:
                print("[*] Yafu SIQS is working.")
            return True
        else:
            if self.verbose:
                print("[*] Yafu SIQS is not working.")
            return False

    def checkyafu(self):
        # Check if yafu exists and we can execute it
        if os.path.isfile(self.yafubin) and os.access(self.yafubin, os.X_OK):
            return True
        else:
            return False

    def benchmarksiqs(self):
        # NYI 
        # return the time to factor a 256-bit RSA modulus
        return

    def doattack(self):
        with open(os.devnull, 'w') as DN:
            try:
                yafurun = subprocess.check_output(
                    [self.yafubin, f'siqs({self.n})',
                     '-siqsT', str(self.maxtime),
                     '-threads', str(self.threads)], stderr=DN
                ).decode('utf-8')
            except subprocess.CalledProcessError as e:
                if self.verbose:
                    print(f"[-] Error running Yafu: {e}")
                return

            primesfound = []

            if 'input too big for SIQS' in yafurun:
                if self.verbose:
                    print("[-] Modulus too big for SIQS method.")
                return

            for line in yafurun.splitlines():
                if re.search(r'^P[0-9]+\ =\ [0-9]+$', line):
                    primesfound.append(int(line.split('=')[1].strip()))

            if len(primesfound) == 2:
                self.p = primesfound[0]
                self.q = primesfound[1]
                if self.verbose:
                    print(f"[+] Found primes: p = {self.p}, q = {self.q}")

            elif len(primesfound) > 2:
                if self.verbose:
                    print("[*] > 2 primes found. Is the key multiprime?")

            else:
                if self.verbose:
                    print("[*] SIQS did not factor the modulus.")

        return

import matplotlib.pyplot as plt
import numpy as np
import math

class Algoritm:
    l = 0
    d = 0
    outputFile = open("output.txt", "w")
    enabled = True

    def __init__(self, nrCromozomi, a, b, coeficienti, p, probIncrucisare, probMutatie, nrEtape):
        self.nrCromozomi = nrCromozomi
        self.a = a
        self.b = b
        self.coeficienti = coeficienti
        self.f = lambda x: coeficienti[0]*x*x + coeficienti[1]*x + coeficienti[2]
        self.cromozomi = [[x, self.f(x), ""] for x in np.random.uniform(self.a, self.b, nrCromozomi)]
        self.p = p
        self.probIncrucisare = probIncrucisare
        self.probMutatie = probMutatie
        self.nrEtape = nrEtape

    def codificare(self):
        for cromozom in self.cromozomi:
            interval = int((cromozom[0] - self.a) // self.d)
            bi = format(interval, '0' + str(self.l) + 'b')
            cromozom[2] = bi

    def decodificare(self):
        for cromozom in self.cromozomi:
            bi = cromozom[2]
            interval = int(bi, 2)
            cromozom[0] = self.a + interval * self.d
            cromozom[1] = self.f(cromozom[0])

    def selectie(self):
        F = sum([cromozom[1] for cromozom in self.cromozomi])
        fitnessRelativ = [cromozom[1]/F for cromozom in self.cromozomi]
        elitist = max(self.cromozomi, key=lambda cromozom : cromozom[1])
        probabilitati = np.cumsum(fitnessRelativ)

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Probabilitati selectie\n")
            i = 0
            for p in fitnessRelativ:
                i = i + 1
                Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + "probabilitate= " + str(p) + "\n")
            Algoritm.outputFile.write("\n")

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Intervale probabilitati selectie\n")
            Algoritm.outputFile.write("0" + " ")
            for q in probabilitati:
                Algoritm.outputFile.write(str(q) + " ")
            Algoritm.outputFile.write("\n" + "\n")

        u = np.random.uniform(low=0, high=1, size=self.nrCromozomi - 1) + np.finfo(float).eps
        cromozomiSelectati = [self.cromozomi[np.searchsorted(probabilitati, ui)] for ui in u]
        cromozomiSelectati.append(elitist)

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Cromozomi selectati\n")
            for ui in u:
                Algoritm.outputFile.write("u=" + str(ui) + " selectam cromozomul " + str(np.searchsorted(probabilitati, ui) + 1) + "\n")
            Algoritm.outputFile.write("\n")

        self.cromozomi = cromozomiSelectati
        if Algoritm.enabled == True:
            i = 0
            Algoritm.outputFile.write("Dupa selectie\n")
            for cromozom in self.cromozomi:
                i = i + 1
                Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + str(cromozom[2]) + " x= " + str(cromozom[0]) + " f= " + str(cromozom[1]) + "\n")
            Algoritm.outputFile.write("\n")

    def incrucisare(self):
        elitist = self.cromozomi[-1]
        self.cromozomi.pop()
        probabilitateIncrucisare = np.random.rand(self.nrCromozomi)
        participanti = [(index, cromozom) for index, (cromozom, prob) in enumerate(zip(self.cromozomi, probabilitateIncrucisare)) if prob < self.probIncrucisare]
        neparticipanti = [cromozom for cromozom, prob in zip(self.cromozomi, probabilitateIncrucisare) if prob >= self.probIncrucisare]
        neparticipanti.append(elitist)

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Probabilitatea de incrucisare " + str(self.probIncrucisare) + "\n")
            i = 0
            j = -1
            for prob in probabilitateIncrucisare:
                i = i + 1
                j = j + 1
                if (j <= len(self.cromozomi) - 1):
                    Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + str(self.cromozomi[j][2]) + " u= " + str(prob) + " ")
                    if prob < self.probIncrucisare:
                        Algoritm.outputFile.write("<" + str(self.probIncrucisare) + " participa\n")
                    else:
                        Algoritm.outputFile.write(">=" + str(self.probIncrucisare) + " nu participa\n")
            Algoritm.outputFile.write("\n")

        while len(participanti) >= 2:
            iParticipanti = np.random.choice(len(participanti), 2, replace=False)
            participant1 = participanti.pop(iParticipanti[0])
            participant2 = participanti.pop(iParticipanti[1]-1)

            punctRupere = np.random.randint(0, self.l)

            if Algoritm.enabled == True:
                Algoritm.outputFile.write("Recombinare dintre cromozomul " + str(participant1[0]+1) + " si cromozomul " + str(participant2[0]+1) + ":" + "\n")
                Algoritm.outputFile.write(str(participant1[1][2]) + " " + str(participant2[1][2]) + " punct= " + str(punctRupere) + "\n")

            participant1[1][2], participant2[1][2] = participant1[1][2][:punctRupere] + participant2[1][2][punctRupere:], participant2[1][2][:punctRupere] + participant1[1][2][punctRupere:]

            neparticipanti.extend([participant1[1], participant2[1]])

            if Algoritm.enabled == True:
                Algoritm.outputFile.write("Rezultat: " + str(participant1[1][2]) + " " + str(participant2[1][2]) + "\n")

        else:
            if len(participanti) == 1:
                neparticipanti.append(participanti[0][1])

        self.cromozomi = neparticipanti
        self.decodificare()

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("\n")
            i = 0
            Algoritm.outputFile.write("Dupa recombinare\n")
            for cromozom in self.cromozomi:
                i = i + 1
                Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + str(cromozom[2]) + " x= " + str(cromozom[0]) + " f= " + str(cromozom[1]) + "\n")
            Algoritm.outputFile.write("\n")

    def mutatie(self):
        probabilitateMutatie = np.random.rand(self.nrCromozomi)
        iParticipanti = np.where(probabilitateMutatie < self.probMutatie)[0]

        for iParticipant in iParticipanti:
            nrPuncteMutatie = np.random.randint(1, self.l/2+1)
            puncteMutatie = np.random.choice(self.l, size=nrPuncteMutatie, replace=True)
            Ci = [int(bit) for bit in self.cromozomi[iParticipant][2]]

            for punct in puncteMutatie:
                Ci[punct] = 1 - int(Ci[punct])

            self.cromozomi[iParticipant][2] = ''.join(map(str, Ci))
            self.decodificare()

        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Probabilitatea de mutatie pentru fiecare gena " + str(self.probMutatie) + "\n")
            Algoritm.outputFile.write("Au fost modificati cromozomii:" + "\n")

            for iParticipant in iParticipanti:
                Algoritm.outputFile.write(str(iParticipant) + "\n")

            Algoritm.outputFile.write("\n")
            Algoritm.outputFile.write("Dupa mutatie:" + "\n")
            i = 0
            for cromozom in self.cromozomi:
                i = i + 1
                Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + str(cromozom[2]) + " x= " + str(cromozom[0]) + " f= " + str(cromozom[1]) + "\n")
            Algoritm.outputFile.write("\n")

    def getMaximum(self):
        if Algoritm.enabled == True:
            Algoritm.outputFile.write("Evolutia maximului si a mediei" + "\n")
        Algoritm.outputFile.write("Maximum: " + str(max(self.cromozomi, key=lambda cromozom: cromozom[1])[1]) + " ")
        return max(self.cromozomi, key=lambda cromozom: cromozom[1])[1]

    def getAverage(self):
        Algoritm.outputFile.write("Media: " + str(np.mean([cromozom[1] for cromozom in self.cromozomi])) + "\n")
        return np.mean([cromozom[1] for cromozom in self.cromozomi])

    def populatieInitiala(self):
        self.codificare()
        i = 0
        Algoritm.outputFile.write("Populatia initiala\n")
        for cromozom in self.cromozomi:
            i = i + 1
            Algoritm.outputFile.write("Cromozomul " + str(i) + ": " + str(cromozom[2]) + " x= " + str(cromozom[0]) + " f= " + str(cromozom[1]) + "\n")
        Algoritm.outputFile.write("\n")

def citireDate():
    with open("input.txt", "r") as file:
        nrCromozomi = int(file.readline().strip())
        a, b = [float(x) for x in file.readline().strip().split(' ')]
        coeficienti = [int(x) for x in file.readline().strip().split(' ')]
        p = float(file.readline().strip())
        probIncrucisare = float(file.readline().strip())
        probMutatie = float(file.readline().strip())
        nrEtape = int(file.readline().strip())

        Algoritm.l = math.ceil(math.log2((b-a)*10**p))
        Algoritm.d = (b-a)/(2**Algoritm.l)

        Alg = Algoritm(nrCromozomi, a, b, coeficienti, p, probIncrucisare, probMutatie, nrEtape)

    return Alg

def main():
    Alg = citireDate()
    Alg.populatieInitiala()
    Maximum = []
    Average = []
    for _ in range(Alg.nrEtape):
        Alg.selectie()
        Alg.incrucisare()
        Alg.mutatie()
        Maximum.append(Alg.getMaximum())
        Average.append(Alg.getAverage())
        Algoritm.enabled = False
    Algoritm.outputFile.close()

    plt.figure(figsize=(10, 6))
    plt.plot(Maximum, label='Maxim')
    plt.plot(Average, label='Mediu')
    plt.xlabel('Etapa')
    plt.ylabel('Valoare')
    plt.title('Evolutia valorilor maxime și medii pe etape')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

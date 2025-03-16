
from parser import stpcommands
from ciphers.cipher import AbstractCipher

from parser.stpcommands import getStringRightRotate as rotr
from parser.stpcommands import getStringLeftRotate as rotl


class GFRX_diffCipher(AbstractCipher):
    name = "GFRX_diff"

    def getFormatString(self):
        return ['x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 'w1', 'w2', 'w3']

    def createSTP(self, stp_filename, parameters):
        wordsize = parameters["wordsize"]
        rounds = parameters["rounds"]
        weight = parameters["sweight"]
        with open(stp_filename, 'w') as stp_file:
            stp_file.write("% Input File for STP\n% (GFRX) w={}  rounds={}\n\n\n".format(wordsize, rounds))

            x1 = ["x1{}".format(i) for i in range(rounds + 1)]
            x2 = ["x2{}".format(i) for i in range(rounds + 1)]
            x3 = ["x3{}".format(i) for i in range(rounds + 1)]
            x4 = ["x4{}".format(i) for i in range(rounds + 1)]

            t1 = ["t1{}".format(i) for i in range(rounds)]
            t2 = ["t2{}".format(i) for i in range(rounds)]
            t3 = ["t3{}".format(i) for i in range(rounds)]
            t4 = ["t4{}".format(i) for i in range(rounds)]
            t5 = ["t5{}".format(i) for i in range(rounds)]
            t6 = ["t6{}".format(i) for i in range(rounds)]
            t7 = ["t7{}".format(i) for i in range(rounds)]
            t8 = ["t8{}".format(i) for i in range(rounds)]
            t9 = ["t9{}".format(i) for i in range(rounds)]
            t10 = ["t10{}".format(i) for i in range(rounds)]
            t11 = ["t11{}".format(i) for i in range(rounds)]
            t12 = ["t12{}".format(i) for i in range(rounds)]
            t13 = ["t13{}".format(i) for i in range(rounds)]
            t14 = ["t14{}".format(i) for i in range(rounds)]
            t15 = ["t15{}".format(i) for i in range(rounds)]
            t16 = ["t16{}".format(i) for i in range(rounds)]
            t17 = ["t17{}".format(i) for i in range(rounds)]
            t18 = ["t18{}".format(i) for i in range(rounds)]
            t19 = ["t19{}".format(i) for i in range(rounds)]
            t20 = ["t20{}".format(i) for i in range(rounds)]
            t21 = ["t21{}".format(i) for i in range(rounds)]
            t22 = ["t22{}".format(i) for i in range(rounds)]
            t23 = ["t23{}".format(i) for i in range(rounds)]
            t24 = ["t24{}".format(i) for i in range(rounds)]
            t25 = ["t25{}".format(i) for i in range(rounds)]
            t26 = ["t26{}".format(i) for i in range(rounds)]
            t27 = ["t27{}".format(i) for i in range(rounds)]
            t28 = ["t28{}".format(i) for i in range(rounds)]
            w1 = ["w1{}".format(i) for i in range(rounds)]
            w2 = ["w2{}".format(i) for i in range(rounds)]
            w3 = ["w3{}".format(i) for i in range(rounds)]
            inimp = ["inimp{}".format(i) for i in range(1)]
            outimp = ["outimp{}".format(i) for i in range(1)]

            stpcommands.setupVariables(stp_file, x1, wordsize)
            stpcommands.setupVariables(stp_file, x2, wordsize)
            stpcommands.setupVariables(stp_file, x3, wordsize)
            stpcommands.setupVariables(stp_file, x4, wordsize)
            stpcommands.setupVariables(stp_file, t1, wordsize)
            stpcommands.setupVariables(stp_file, t2, wordsize)
            stpcommands.setupVariables(stp_file, t3, wordsize)
            stpcommands.setupVariables(stp_file, t4, wordsize)
            stpcommands.setupVariables(stp_file, t5, wordsize)
            stpcommands.setupVariables(stp_file, t6, wordsize)
            stpcommands.setupVariables(stp_file, t7, wordsize)
            stpcommands.setupVariables(stp_file, t8, wordsize)
            stpcommands.setupVariables(stp_file, t9, wordsize)
            stpcommands.setupVariables(stp_file, t10, wordsize)
            stpcommands.setupVariables(stp_file, t11, wordsize)
            stpcommands.setupVariables(stp_file, t12, wordsize)
            stpcommands.setupVariables(stp_file, t13, wordsize)
            stpcommands.setupVariables(stp_file, t14, wordsize)
            stpcommands.setupVariables(stp_file, t15, wordsize)
            stpcommands.setupVariables(stp_file, t16, wordsize)
            stpcommands.setupVariables(stp_file, t17, wordsize)
            stpcommands.setupVariables(stp_file, t18, wordsize)
            stpcommands.setupVariables(stp_file, t19, wordsize)
            stpcommands.setupVariables(stp_file, t20, wordsize)
            stpcommands.setupVariables(stp_file, t21, wordsize)
            stpcommands.setupVariables(stp_file, t22, wordsize)
            stpcommands.setupVariables(stp_file, t23, wordsize)
            stpcommands.setupVariables(stp_file, t24, wordsize)
            stpcommands.setupVariables(stp_file, t25, wordsize)
            stpcommands.setupVariables(stp_file, t26, wordsize)
            stpcommands.setupVariables(stp_file, t27, wordsize)
            stpcommands.setupVariables(stp_file, t28, wordsize)
            stpcommands.setupVariables(stp_file, w1, wordsize)
            stpcommands.setupVariables(stp_file, w2, wordsize)
            stpcommands.setupVariables(stp_file, w3, wordsize)



            # Ignore MSB
            stpcommands.setupWeightComputation(stp_file, weight, w1 + w2 + w3, wordsize)

            for i in range(rounds):
                self.setupRound(stp_file, x1[i], x2[i], x3[i], x4[i], x1[i+1], x2[i+1], x3[i+1], x4[i+1], t1[i], t2[i], t3[i], t4[i], t5[i], t6[i], t7[i], t8[i], t9[i], t10[i], t11[i], t12[i], t13[i], t14[i], t15[i], t16[i], t17[i], t18[i], t19[i], t20[i], t21[i], t22[i], t23[i], t24[i], t25[i], t26[i], t27[i], t28[i], w1[i], w2[i], w3[i], wordsize)
            # No all zero characteristic
            stpcommands.assertNonZero(stp_file, x1 + x2 + x3 + x4, wordsize)
            if parameters["iterative"]:
                stpcommands.assertVariableValue(stp_file, x1[0], x1[rounds])
                stpcommands.assertVariableValue(stp_file, x2[0], x2[rounds])
                stpcommands.assertVariableValue(stp_file, x3[0], x3[rounds])
                stpcommands.assertVariableValue(stp_file, x4[0], x4[rounds])
            for key, value in parameters["fixedVariables"].items():
                stpcommands.assertVariableValue(stp_file, key, value)
            for char in parameters["blockedCharacteristics"]:
                stpcommands.blockCharacteristic(stp_file, char, wordsize)

            #stp_file.write("ASSERT((x1)= 0hex00000000);\n")

            stpcommands.setupQuery(stp_file)
        return

    def setupRound(self, stp_file, x1, x2, x3, x4, y1, y2, y3, y4, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, w1, w2, w3, wordsize):
        command = ""
        command += stpcommands.branch_diff(x2, t1, t2, wordsize)
        command += stpcommands.branch_diff(t2, t3, t4, wordsize)
        command += stpcommands.branch_diff(t4, t5, t6, wordsize)
        command += stpcommands.lrotate(t1, t7, 1, wordsize)
        command += stpcommands.lrotate(t3, t8, 8, wordsize)
        command += stpcommands.lrotate(t5, t10, 2, wordsize)
        command += stpcommands.and_diff(t7, t8, t9, w1, wordsize)
        command += stpcommands.xor_diff(x1, t9, t11, wordsize)
        command += stpcommands.xor_diff(t10, t11, y3, wordsize)

        command += stpcommands.branch_diff(x3, t12, t13, wordsize)
        command += stpcommands.branch_diff(t13, t14, t15, wordsize)
        command += stpcommands.branch_diff(t15, t16, t17, wordsize)
        command += stpcommands.lrotate(t12, t18, 1, wordsize)
        command += stpcommands.lrotate(t14, t19, 8, wordsize)
        command += stpcommands.lrotate(t16, t21, 2, wordsize)
        command += stpcommands.and_diff(t18, t19, t20, w2, wordsize)
        command += stpcommands.xor_diff(x4, t20, t22, wordsize)
        command += stpcommands.xor_diff(t21, t22, y2, wordsize)

        command += stpcommands.rrotate(t6, t23, 8, wordsize)
        command += stpcommands.branch_diff(t17, t24, t25, wordsize)
        command += stpcommands.add_diff(t23, t24, t27, w3, wordsize)
        command += stpcommands.lrotate(t25, t26, 3, wordsize)
        command += stpcommands.branch_diff(t27, t28, y1, wordsize)
        command += stpcommands.xor_diff(t28, t26, y4, wordsize)

        stp_file.write(command)
        return

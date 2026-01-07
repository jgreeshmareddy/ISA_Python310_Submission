import json
import sys

REG = [0]*8
W = [0]*8
B = [0]*8

def dbg(msg):
    print("[INTERPRETER]", msg)

def illegal(msg):
    print("[ILLEGAL]", msg)
    sys.exit(1)

def run(machine_file, out_file):
    dbg("Starting execution...")

    with open(machine_file, "r") as f:
        code = [x.strip() for x in f.readlines() if x.strip()]

    pc = 0
    while pc < len(code):
        line = code[pc]
        parts = line.split()
        instr = parts[0]

        if instr == "FF":  # HALT
            dbg("HALT reached")
            break

        elif instr == "00":  # LOAD
            R = int(parts[1][1])
            IMM = int(parts[2][1:])
            REG[R] = IMM

        elif instr == "01":  # STORE_W
            R = int(parts[1][1])
            A = int(parts[2])
            W[A] = REG[R]

        elif instr == "02":  # STORE_B
            R = int(parts[1][1])
            A = int(parts[2])
            B[A] = REG[R]

        elif instr == "03":  # MAC
            RD = int(parts[1][1])
            RS1 = int(parts[2][1])
            RS2 = int(parts[3][1])
            REG[RD] = REG[RS1] * REG[RS2]

        elif instr == "04":  # ADD
            RD = int(parts[1][1])
            RS1 = int(parts[2][1])
            RS2 = int(parts[3][1])
            REG[RD] = REG[RS1] + REG[RS2]

        elif instr == "05":  # SUB
            RD = int(parts[1][1])
            RS1 = int(parts[2][1])
            RS2 = int(parts[3][1])
            REG[RD] = REG[RS1] - REG[RS2]

        else:
            illegal("Unknown opcode " + instr)

        pc += 1

    json.dump({
        "registers": REG,
        "weights": W,
        "biases": B
    }, open(out_file, "w"), indent=4)

    dbg("Execution completed.")
    dbg("Output -> " + out_file)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python interpreter.py <program.machine> <out.json>")
        sys.exit(1)

    run(sys.argv[1], sys.argv[2])

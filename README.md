# Zynq7000-Petalinux SHA256D Miner

A hardware-accelerated SHA256d (double-SHA256) cryptocurrency miner for Xilinx Zynq-7000 FPGA. HLS-synthesized hardware modules perform the hashing; Python software controls the FPGA cores via memory-mapped I/O.

## Architecture

```
Python Controller ──mmap(/dev/mem)──> FPGA Cores (x4) ──HLS──> SHA256d Hardware
       │                                    │
  scanShaPrimitives.py              Base addresses:
  IOprimitive.py                    0x40000000 - 0x40030000
  addresses.py
```

## Hardware (HLS C++)

Synthesizable SHA256d implementation for Vivado HLS:

| Module | Purpose |
|--------|---------|
| `sha256impl.cpp` | SHA256 core (32-bit word operations) |
| `sha256d.cpp` | Double-SHA256 wrapper (two passes) |
| `scan_sha256d.cpp` | Nonce scanning loop |
| `groestlHLScod/` | Alternative Groestl hash algorithm |

## Software (Python)

| File | Purpose |
|------|---------|
| `scanShaPrimitives.py` | High-level mining control (start/stop/step/read) |
| `IOprimitive.py` | Low-level FPGA memory I/O via `/dev/mem` mmap |
| `addresses.py` | FPGA register addresses from Vivado constraints |

## FPGA Register Map

| Register | Offset | Description |
|----------|--------|-------------|
| `ACTUAL` | 0x10 | Current nonce counter |
| `TARG` | 0x20 | Target hash (difficulty) |
| `GOLDEN` | 0x40 | Found solution (non-zero = valid) |
| `ACHASH` | 0x60 | Computed hash output |
| `HEAD` | 0x80 | Block header input (76 bytes) |

## Features

- **4 parallel FPGA cores** — simultaneous nonce scanning
- **Memory-mapped I/O** — direct register access via `/dev/mem`
- **HLS synthesis** — C++ to hardware, deployable on Zynq-7000
- **Modular** — add more FPGA cards for linear scaling

## Documentation

Detailed project report included in repository.

---

*Miner SHA256d con accelerazione hardware per FPGA Xilinx Zynq-7000. Moduli hardware sintetizzati via HLS eseguono l'hashing; software Python controlla i core FPGA tramite I/O memory-mapped. Supporta 4 core paralleli con interfaccia a registri per il controllo del mining.*

# Gate 7′ hardware and resource report

## Host class

- architecture: x86-64;
- virtualization: KVM virtual machine;
- visible CPUs: 5;
- CPU model: Intel Xeon Platinum 8573C;
- visible memory: 6 219 544 KiB;
- swap: 0 KiB;
- kernel: Linux 6.18.35.

No GPU was required or used.

## Toolchain

- CPython 3.13.5;
- Go 1.23.2 linux/amd64;
- GCC-compatible `cc` 14.2.0;
- Z3 runtime 4.13.3.0 exposed as `libz3.so.4`;
- standard POSIX `bash` and `sha256sum`.

## Reference clean-copy run

- elapsed wall clock: 6.48 seconds;
- user CPU: 8.16 seconds;
- system CPU: 1.28 seconds;
- maximum resident set: 113 372 KiB;
- swaps: 0;
- socket messages sent/received: 0/0.

Resource values are observations from one run, not minimum requirements or
performance guarantees.

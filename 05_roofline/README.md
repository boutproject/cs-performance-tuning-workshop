# Roofline analysis

## Introduction

Roofline analysis is a technique for assessing the performance of code kernels.
It attempts to quantify what is meant be "good performance" by comparing the
achieved FLOPs to the theoretical maximum value accounting for processor speed
and memory bandwidth.

There are four main motivations for using roofline analysis [Samuel Williams, The Roofline Model: A Bridge between Computer Science, Applied Math, and Computational Science, SciDAC Meeting, July 2020](https://crd.lbl.gov/assets/Uploads/SciDAC20-Roofline-SWWilliams.pdf):

> 1. Determine when we're done optimizing code  
>   - Assess performance relative to machine capabilities
>   - Track progress towards optimality
>   - Motivate need for algorithmic changes
> 2. Identify performance bottlenecks & motivate software optimizations
> 3. Understand performance differences between Architectures, Programming Models, implementations, etc.
>   - Why do some Architectures/Implementations move more data than others?
>   - Why do some compilers outperform others?
> 4. Predict performance on future machines / architectures

The key idea is that a code kernel's performance can be limited by one of two things:

1. The rate of performing FLOPs (measured in Flops/s)
2. The rate at which data can be loaded into memory in order to use it in
   calculations (measures in Bytes/s)

The ratio of FLOPs to Bytes moves is called the arithmetic intensity (measured
in FLOPs/Byte).

In roofline analysis, we plot performance achieved in FLOPs/s on the y axis
against arithmetic intensity in FLOPs/Byte on the x axis.
On this graph, the processor's constant peak FLOP rate is a horizontal line,
while constant memory bandwidth is a diagonal line
(`y[FLOPs/s]=cst[Bytes/s]*x[FLOPs/Byte]`).

We thus have a roofline plot

```
Achieved     ^                   
performance  |      ___________Proc max FLOPs/s
[FLOPs/s]    |     /
             |    /
             |   /
             |  / <-- memory bandwidth Bytes/s
             | /
             |/________________________________
                
                Arithmetic 
                intensity 
                [FLOPs/Byte]
```

The actual performance for a code kernel will be a point on this graph on or
below the roofline.
Whether this point is below the memory bandwidth limit (the diagonal line) or
peak performance limit gives information about code performance in a given
parameter regime, at a given thread count and on a particular architecture.
It also gives information about how (or whether!) to optimize a kernel.
If a kernel is memory bandwidth bound (i.e. on the diagonal line),
an increase in achieved FLOPs will come from increasing the arithmetic
intensity, either by utilizing data per memory load or by changing the
algorithm.

### Cache levels

The above speaks about "memory bandwidth", when in fact there are several levels
of memory, each with differing bandwidths.
These means there will be several diagonal lines on the roofline plot.

### Multiple threads

The memory bandwidth and peak performance lines refer to the available resources.
Therefore, if the number of cores doubles, the peak attainable performance
should double too.

## Producing roofline plots

There are a few tools for producing roofline plots.
These range from being essentially manual (LIKWID, reading your machine's
specs...) to automated tools like NVIDIA's Nsight Compute and Intel's Advisor.
Nsight Compute is only for GPUs, but Intel's Advisor works for CPUs too.
All software mentioned here is available for free (perhaps requiring
registration.
Intel Advisor is part of oneAPI.

### Reading machine specs

### Empirical Roofline Tool

### NVidia NSight

### Intel Advisor

### LIKWID






## Links

Here are some links on roofline. The repo I used in the end is this one:

https://bitbucket.org/berkeleylab/cs-roofline-toolkit/src/master/

 

Their website has a useful introduction here and in the subsections:

https://crd.lbl.gov/departments/computer-science/par/research/roofline/

 

The publication section has lots of presentations. Here’s one that seems to have their standard intro slides:

https://crd.lbl.gov/assets/Uploads/SciDAC20-Roofline-SWWilliams.pdf

Slide 36 (What is good performance?) makes that point that “getting high performance” and “making good use of the machine” are two different things.

 

The LIKWID suite I was thinking of is here: https://hpc.fau.de/research/tools/likwid/

https://github.com/RRZE-HPC/likwid

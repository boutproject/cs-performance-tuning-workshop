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
peak performance limit gives on information about code performance in a given
parameter regime, at a given thread count and on a particular architecture.

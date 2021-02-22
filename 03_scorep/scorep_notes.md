# Score-P with BOUT++/STORM

See workshop slides for intro.

Score-P configuration with BOUT++ was set up with a previous project (with EPCC?). This
configuration only instruments MPI calls, because fully instrumenting the code makes runs
unmanageably slow. To fully instrument the code, edit `make.config` to remove the
`--nocompiler` flag. Then need to filter...

### Filtering

Filtering is needed both to prevent Score-P from running out of memory to store its
profiling information, and to prevent excessive overhead from instrumentation making the
profiling uninformative.

Running with a short enough `timestep` and `nout` with full instrumentation (a few hundred
rhs calls should be plenty) should let Score-P produce some output.

> Without filtering the runs may be very slow (observed with icc/intelmpi on DINE).
> However on Marconi with gcc/openmpi the unfiltered run took only about 9 mins, compared
> to 1 min 50 s for a plain, non-Score-P run.

The output with full instrumentation can then be used to find out which calls need to be
filtered. If example output is in the `scorep-storm` directory then calling

```
scorep-score -r scorep-storm/profile.cubex
```

Will produce a report showing Score-P's memory usage and the memory usage and time from
tracing each instrumented function call. Calls with less than ~1 microsecond of
`time/visit` should probably be filtered as the overhead is greater than the time spent in
them.

> With gcc/openmpi on Marconi, the instrumented calls introducing the most overhead were
> operator()(stencil f), which are used inside tight loops by the derivative functions.
> Currently not clear if instrumentation prevents these being inlined (any way to test
> this?).

Calls can be filtered using a 'filter file', e.g.

```
SCOREP_REGION_NAMES_BEGIN
  EXCLUDE
    *operator()*
    *tridagCoefs*
SCOREP_REGION_NAMES_END
```

(see workshop slides for more info). Calls can also be filtered by source file.

To test a filter file (for example called `scorep.filt`) it is useful to use
`scorep-score` again like

```
scorep-score -r -f scorep.filt scorep-storm/profile.cubex
```

This will produce a report as if `scorep` had been run using the filter file, so it is
possible to check if the memory usage has been reduced to a reasonable level. Note that
memory usage increases with the length of the run (presumably linearly apart from
cost of initialisation routines), so need to remember to scale up if looking at a
`profile.cubex` from a very short initial attempt. The memory usage needs to be kept down
to prevent Score-P from flushing buffers to disk, which may produce inconsistent profiles.

A filter file that has allowed Score-P to produce reasonable profiles for STORM is
included in this directory: `scorep.filt`.

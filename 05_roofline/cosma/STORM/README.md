Roofline plots for STORM, corresponding to incremental "improvements" to BOUT.

To get the `BOUT_FOR` loop to vectorize with Intel 2018, we replaced the
`BOUT_FOR` marco with its definition, and inserted the `#pragma ivdep` pragma
between the first and second loop.
This tells the compiler that the second loop does not contain any data
dependences.
We could not insert this in the `BOUT_FOR` macro, as that is defined using for
loops that don't have `{}` brackets, meaning inserting an extra line breaks the
macro.
(The kernel of work in the `BOUT_FOR` macro are not arguments to the macro --
we cannot insert the pragma without changing the definition of the macro
everywhere it is called.)

The roofline in these subfolders correspond to incrementally adding the pragma
line to more loops.
Of these, vectorizing only gives a noticable speed up to the standard
derivative... but each kernel is a small component of the code, so the speed up
for any loop is minimal!

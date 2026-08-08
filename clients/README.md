# Anticaptrad client matrix

All client slices consume `anticaptrad/act-interfaces`. No `act-lib` repository exists today, so the Zed package deliberately imports only the real interface package.

TypeScript supports Node.js, Deno, Bun, and edge runtimes through `clients/typescript/runtimes/`. Those runtime names are not separate Zed targets.

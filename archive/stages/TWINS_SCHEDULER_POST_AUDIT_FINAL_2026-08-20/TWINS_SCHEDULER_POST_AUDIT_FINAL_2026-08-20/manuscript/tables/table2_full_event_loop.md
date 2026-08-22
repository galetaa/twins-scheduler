<!-- Fuller two-round event-loop outcomes. -->

| Grammar | Variant | Violation | Decisions | POLKA | COMMIT |
|---|---|---|---|---|---|
| G_T_TYPE_SPECIFIC | BASELINE | no | H1=0 | [0] | [0] |
| G_D_ROUND0_EDGE_OFF | BASELINE | no | H3=1, P=1 | [1] | [1] |
| G_D_ROUND0_EDGE_ON | BASELINE | no | H1=0, P=0 | [0] | [0] |
| G_T_TYPE_SPECIFIC | MISSING_LOCK_UPDATE | YES | H1=0, H3=1, P=1 | [0, 1] | [0, 1] |
| G_D_ROUND0_EDGE_OFF | MISSING_LOCK_UPDATE | no | H3=1, P=1 | [1] | [1] |
| G_D_ROUND0_EDGE_ON | MISSING_LOCK_UPDATE | no | H1=0, P=0 | [0] | [0] |

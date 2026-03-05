#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _NMDA_CA1_pyr_SC_2_comp_midway_reg(void);
extern void _NMDA_CA1_pyr_SC_2_comp_reg(void);
extern void _NMDA_CA1_pyr_SC_midway_reg(void);
extern void _NMDA_CA1_pyr_SC_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"NMDA_CA1_pyr_SC_2_comp_midway.mod\"");
    fprintf(stderr, " \"NMDA_CA1_pyr_SC_2_comp.mod\"");
    fprintf(stderr, " \"NMDA_CA1_pyr_SC_midway.mod\"");
    fprintf(stderr, " \"NMDA_CA1_pyr_SC.mod\"");
    fprintf(stderr, "\n");
  }
  _NMDA_CA1_pyr_SC_2_comp_midway_reg();
  _NMDA_CA1_pyr_SC_2_comp_reg();
  _NMDA_CA1_pyr_SC_midway_reg();
  _NMDA_CA1_pyr_SC_reg();
}

#if defined(__cplusplus)
}
#endif

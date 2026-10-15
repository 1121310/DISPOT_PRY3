\ Model TNEP_MILP_bigM_Villasana
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x85d3178cdfc91dfc
Minimize
  150 w[0,1] + 300 w[0,2] + 450 w[0,3] + 600 w[0,4] + 150 w[1,1]
   + 300 w[1,2] + 450 w[1,3] + 600 w[1,4] + 305 w[2,1] + 610 w[2,2]
   + 915 w[2,3] + 100 w[3,1] + 200 w[3,2] + 300 w[3,3]
Subject To
 flujo_existente_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + Pa[0] = 0
 flujo_existente_1-4_1: - 1.666666666666667 theta[0]
   + 1.666666666666667 theta[3] + Pa[1] = 0
 flujo_existente_1-5_2: - 5 theta[0] + 5 theta[4] + Pa[2] = 0
 flujo_existente_2-3_3: - 5 theta[1] + 5 theta[2] + Pa[3] = 0
 flujo_existente_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + Pa[4] = 0
 flujo_existente_3-5_5: - 5 theta[2] + 5 theta[4] + Pa[5] = 0
 cap_sup_6-2_1: - w[0,1] + 3.333333333333333 dtheta[0,1] <= 0
 cap_inf_6-2_1: w[0,1] + 3.333333333333333 dtheta[0,1] >= 0
 cap_sup_6-2_2: - 2 w[0,2] + 6.666666666666667 dtheta[0,2] <= 0
 cap_inf_6-2_2: 2 w[0,2] + 6.666666666666667 dtheta[0,2] >= 0
 cap_sup_6-2_3: - 3 w[0,3] + 10 dtheta[0,3] <= 0
 cap_inf_6-2_3: 3 w[0,3] + 10 dtheta[0,3] >= 0
 cap_sup_6-2_4: - 4 w[0,4] + 13.33333333333333 dtheta[0,4] <= 0
 cap_inf_6-2_4: 4 w[0,4] + 13.33333333333333 dtheta[0,4] >= 0
 bigM_sup_6-2: - theta[1] + theta[5] + w[0,1] + w[0,2] + w[0,3] + w[0,4]
   - dtheta[0,1] - dtheta[0,2] - dtheta[0,3] - dtheta[0,4] <= 1
 bigM_inf_6-2: - theta[1] + theta[5] - w[0,1] - w[0,2] - w[0,3] - w[0,4]
   - dtheta[0,1] - dtheta[0,2] - dtheta[0,3] - dtheta[0,4] >= -1
 unicidad_6-2: w[0,1] + w[0,2] + w[0,3] + w[0,4] <= 1
 cap_sup_6-4_1: - w[1,1] + 3.333333333333333 dtheta[1,1] <= 0
 cap_inf_6-4_1: w[1,1] + 3.333333333333333 dtheta[1,1] >= 0
 cap_sup_6-4_2: - 2 w[1,2] + 6.666666666666667 dtheta[1,2] <= 0
 cap_inf_6-4_2: 2 w[1,2] + 6.666666666666667 dtheta[1,2] >= 0
 cap_sup_6-4_3: - 3 w[1,3] + 10 dtheta[1,3] <= 0
 cap_inf_6-4_3: 3 w[1,3] + 10 dtheta[1,3] >= 0
 cap_sup_6-4_4: - 4 w[1,4] + 13.33333333333333 dtheta[1,4] <= 0
 cap_inf_6-4_4: 4 w[1,4] + 13.33333333333333 dtheta[1,4] >= 0
 bigM_sup_6-4: - theta[3] + theta[5] + w[1,1] + w[1,2] + w[1,3] + w[1,4]
   - dtheta[1,1] - dtheta[1,2] - dtheta[1,3] - dtheta[1,4] <= 1
 bigM_inf_6-4: - theta[3] + theta[5] - w[1,1] - w[1,2] - w[1,3] - w[1,4]
   - dtheta[1,1] - dtheta[1,2] - dtheta[1,3] - dtheta[1,4] >= -1
 unicidad_6-4: w[1,1] + w[1,2] + w[1,3] + w[1,4] <= 1
 cap_sup_6-5_1: - w[2,1] + 1.639344262295082 dtheta[2,1] <= 0
 cap_inf_6-5_1: w[2,1] + 1.639344262295082 dtheta[2,1] >= 0
 cap_sup_6-5_2: - 2 w[2,2] + 3.278688524590164 dtheta[2,2] <= 0
 cap_inf_6-5_2: 2 w[2,2] + 3.278688524590164 dtheta[2,2] >= 0
 cap_sup_6-5_3: - 3 w[2,3] + 4.918032786885246 dtheta[2,3] <= 0
 cap_inf_6-5_3: 3 w[2,3] + 4.918032786885246 dtheta[2,3] >= 0
 bigM_sup_6-5: - theta[4] + theta[5] + w[2,1] + w[2,2] + w[2,3]
   - dtheta[2,1] - dtheta[2,2] - dtheta[2,3] <= 1
 bigM_inf_6-5: - theta[4] + theta[5] - w[2,1] - w[2,2] - w[2,3]
   - dtheta[2,1] - dtheta[2,2] - dtheta[2,3] >= -1
 unicidad_6-5: w[2,1] + w[2,2] + w[2,3] <= 1
 cap_sup_3-5_1: - w[3,1] + 5 dtheta[3,1] <= 0
 cap_inf_3-5_1: w[3,1] + 5 dtheta[3,1] >= 0
 cap_sup_3-5_2: - 2 w[3,2] + 10 dtheta[3,2] <= 0
 cap_inf_3-5_2: 2 w[3,2] + 10 dtheta[3,2] >= 0
 cap_sup_3-5_3: - 3 w[3,3] + 15 dtheta[3,3] <= 0
 cap_inf_3-5_3: 3 w[3,3] + 15 dtheta[3,3] >= 0
 bigM_sup_3-5: theta[2] - theta[4] + w[3,1] + w[3,2] + w[3,3] - dtheta[3,1]
   - dtheta[3,2] - dtheta[3,3] <= 1
 bigM_inf_3-5: theta[2] - theta[4] - w[3,1] - w[3,2] - w[3,3] - dtheta[3,1]
   - dtheta[3,2] - dtheta[3,3] >= -1
 unicidad_3-5: w[3,1] + w[3,2] + w[3,3] <= 1
 balance_1: Pa[0] + Pa[1] + Pa[2] = -0.3
 balance_2: - 3.333333333333333 dtheta[0,1] - 6.666666666666667 dtheta[0,2]
   - 10 dtheta[0,3] - 13.33333333333333 dtheta[0,4] - Pa[0] + Pa[3] + Pa[4]
   = -2.4
 balance_3: 5 dtheta[3,1] + 10 dtheta[3,2] + 15 dtheta[3,3] - Pa[3] + Pa[5]
   = 1.25
 balance_4: - 3.333333333333333 dtheta[1,1] - 6.666666666666667 dtheta[1,2]
   - 10 dtheta[1,3] - 13.33333333333333 dtheta[1,4] - Pa[1] - Pa[4] = -1.6
 balance_5: - 1.639344262295082 dtheta[2,1] - 3.278688524590164 dtheta[2,2]
   - 4.918032786885246 dtheta[2,3] - 5 dtheta[3,1] - 10 dtheta[3,2]
   - 15 dtheta[3,3] - Pa[2] - Pa[5] = -2.4
 balance_6: 3.333333333333333 dtheta[0,1] + 6.666666666666667 dtheta[0,2]
   + 10 dtheta[0,3] + 13.33333333333333 dtheta[0,4]
   + 3.333333333333333 dtheta[1,1] + 6.666666666666667 dtheta[1,2]
   + 10 dtheta[1,3] + 13.33333333333333 dtheta[1,4]
   + 1.639344262295082 dtheta[2,1] + 3.278688524590164 dtheta[2,2]
   + 4.918032786885246 dtheta[2,3] = 5.45
Bounds
 theta[0] free
 theta[1] free
 theta[2] free
 theta[3] free
 theta[4] = 0
 theta[5] free
 dtheta[0,1] free
 dtheta[0,2] free
 dtheta[0,3] free
 dtheta[0,4] free
 dtheta[1,1] free
 dtheta[1,2] free
 dtheta[1,3] free
 dtheta[1,4] free
 dtheta[2,1] free
 dtheta[2,2] free
 dtheta[2,3] free
 dtheta[3,1] free
 dtheta[3,2] free
 dtheta[3,3] free
 -1 <= Pa[0] <= 1
 -0.8 <= Pa[1] <= 0.8
 -1 <= Pa[2] <= 1
 -1 <= Pa[3] <= 1
 -1 <= Pa[4] <= 1
 -1 <= Pa[5] <= 1
Binaries
 w[0,1] w[0,2] w[0,3] w[0,4] w[1,1] w[1,2] w[1,3] w[1,4] w[2,1] w[2,2]
 w[2,3] w[3,1] w[3,2] w[3,3]
End

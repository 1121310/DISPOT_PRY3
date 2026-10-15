\ Model TNEP_MINLP_bilineal
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x5e516f9f76ae1e00
Minimize
  150 n[0] + 150 n[1] + 305 n[2] + 100 n[3]
Subject To
 flujo_existente_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + Pa[0] = 0
 flujo_existente_1-4_1: - 1.666666666666667 theta[0]
   + 1.666666666666667 theta[3] + Pa[1] = 0
 flujo_existente_1-5_2: - 5 theta[0] + 5 theta[4] + Pa[2] = 0
 flujo_existente_2-3_3: - 5 theta[1] + 5 theta[2] + Pa[3] = 0
 flujo_existente_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + Pa[4] = 0
 flujo_existente_3-5_5: - 5 theta[2] + 5 theta[4] + Pa[5] = 0
 apertura_6-2: theta[1] - theta[5] + dtheta[0] = 0
 cap_sup_6-2: - n[0] + Pij[0] <= 0
 cap_inf_6-2: n[0] + Pij[0] >= 0
 apertura_6-4: theta[3] - theta[5] + dtheta[1] = 0
 cap_sup_6-4: - n[1] + Pij[1] <= 0
 cap_inf_6-4: n[1] + Pij[1] >= 0
 apertura_6-5: theta[4] - theta[5] + dtheta[2] = 0
 cap_sup_6-5: - n[2] + Pij[2] <= 0
 cap_inf_6-5: n[2] + Pij[2] >= 0
 apertura_3-5: - theta[2] + theta[4] + dtheta[3] = 0
 cap_sup_3-5: - n[3] + Pij[3] <= 0
 cap_inf_3-5: n[3] + Pij[3] >= 0
 balance_1: Pa[0] + Pa[1] + Pa[2] = -0.3
 balance_2: - Pij[0] - Pa[0] + Pa[3] + Pa[4] = -2.4
 balance_3: Pij[3] - Pa[3] + Pa[5] = 1.25
 balance_4: - Pij[1] - Pa[1] - Pa[4] = -1.6
 balance_5: - Pij[2] - Pij[3] - Pa[2] - Pa[5] = -2.4
 balance_6: Pij[0] + Pij[1] + Pij[2] = 5.45
 bilineal_6-2: Pij[0] + [ - 3.333333333333333 n[0] * dtheta[0] ] = 0
 bilineal_6-4: Pij[1] + [ - 3.333333333333333 n[1] * dtheta[1] ] = 0
 bilineal_6-5: Pij[2] + [ - 1.639344262295082 n[2] * dtheta[2] ] = 0
 bilineal_3-5: Pij[3] + [ - 5 n[3] * dtheta[3] ] = 0
Bounds
 -1.5708 <= theta[0] <= 1.5708
 -1.5708 <= theta[1] <= 1.5708
 -1.5708 <= theta[2] <= 1.5708
 -1.5708 <= theta[3] <= 1.5708
 theta[4] = 0
 -1.5708 <= theta[5] <= 1.5708
 n[0] <= 4
 n[1] <= 4
 n[2] <= 3
 n[3] <= 3
 -3.1416 <= dtheta[0] <= 3.1416
 -3.1416 <= dtheta[1] <= 3.1416
 -3.1416 <= dtheta[2] <= 3.1416
 -3.1416 <= dtheta[3] <= 3.1416
 -4 <= Pij[0] <= 4
 -4 <= Pij[1] <= 4
 -3 <= Pij[2] <= 3
 -3 <= Pij[3] <= 3
 -1 <= Pa[0] <= 1
 -0.8 <= Pa[1] <= 0.8
 -1 <= Pa[2] <= 1
 -1 <= Pa[3] <= 1
 -1 <= Pa[4] <= 1
 -1 <= Pa[5] <= 1
Generals
 n[0] n[1] n[2] n[3]
End

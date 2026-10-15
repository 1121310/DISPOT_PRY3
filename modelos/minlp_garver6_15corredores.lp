\ Model TNEP_MINLP_bilineal
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xe13ae2aeb2e6730d
Minimize
  200 n[0] + 190 n[1] + 300 n[2] + 100 n[3] + 340 n[4] + 100 n[5] + 200 n[6]
   + 155 n[7] + 150 n[8] + 295 n[9] + 100 n[10] + 240 n[11] + 315 n[12]
   + 150 n[13] + 305 n[14]
Subject To
 flujo_existente_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + Pa[0] = 0
 flujo_existente_1-4_1: - 1.666666666666667 theta[0]
   + 1.666666666666667 theta[3] + Pa[1] = 0
 flujo_existente_1-5_2: - 5 theta[0] + 5 theta[4] + Pa[2] = 0
 flujo_existente_2-3_3: - 5 theta[1] + 5 theta[2] + Pa[3] = 0
 flujo_existente_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + Pa[4] = 0
 flujo_existente_3-5_5: - 5 theta[2] + 5 theta[4] + Pa[5] = 0
 apertura_1-2: - theta[0] + theta[1] + dtheta[0] = 0
 cap_sup_1-2: - n[0] + Pij[0] <= 0
 cap_inf_1-2: n[0] + Pij[0] >= 0
 apertura_1-3: - theta[0] + theta[2] + dtheta[1] = 0
 cap_sup_1-3: - n[1] + Pij[1] <= 0
 cap_inf_1-3: n[1] + Pij[1] >= 0
 apertura_1-4: - theta[0] + theta[3] + dtheta[2] = 0
 cap_sup_1-4: - 0.8 n[2] + Pij[2] <= 0
 cap_inf_1-4: 0.8 n[2] + Pij[2] >= 0
 apertura_1-5: - theta[0] + theta[4] + dtheta[3] = 0
 cap_sup_1-5: - n[3] + Pij[3] <= 0
 cap_inf_1-5: n[3] + Pij[3] >= 0
 apertura_1-6: - theta[0] + theta[5] + dtheta[4] = 0
 cap_sup_1-6: - 0.7 n[4] + Pij[4] <= 0
 cap_inf_1-6: 0.7 n[4] + Pij[4] >= 0
 apertura_2-3: - theta[1] + theta[2] + dtheta[5] = 0
 cap_sup_2-3: - n[5] + Pij[5] <= 0
 cap_inf_2-3: n[5] + Pij[5] >= 0
 apertura_2-4: - theta[1] + theta[3] + dtheta[6] = 0
 cap_sup_2-4: - n[6] + Pij[6] <= 0
 cap_inf_2-4: n[6] + Pij[6] >= 0
 apertura_2-5: - theta[1] + theta[4] + dtheta[7] = 0
 cap_sup_2-5: - n[7] + Pij[7] <= 0
 cap_inf_2-5: n[7] + Pij[7] >= 0
 apertura_2-6: - theta[1] + theta[5] + dtheta[8] = 0
 cap_sup_2-6: - n[8] + Pij[8] <= 0
 cap_inf_2-6: n[8] + Pij[8] >= 0
 apertura_3-4: - theta[2] + theta[3] + dtheta[9] = 0
 cap_sup_3-4: - 0.82 n[9] + Pij[9] <= 0
 cap_inf_3-4: 0.82 n[9] + Pij[9] >= 0
 apertura_3-5: - theta[2] + theta[4] + dtheta[10] = 0
 cap_sup_3-5: - n[10] + Pij[10] <= 0
 cap_inf_3-5: n[10] + Pij[10] >= 0
 apertura_3-6: - theta[2] + theta[5] + dtheta[11] = 0
 cap_sup_3-6: - n[11] + Pij[11] <= 0
 cap_inf_3-6: n[11] + Pij[11] >= 0
 apertura_4-5: - theta[3] + theta[4] + dtheta[12] = 0
 cap_sup_4-5: - 0.75 n[12] + Pij[12] <= 0
 cap_inf_4-5: 0.75 n[12] + Pij[12] >= 0
 apertura_4-6: - theta[3] + theta[5] + dtheta[13] = 0
 cap_sup_4-6: - n[13] + Pij[13] <= 0
 cap_inf_4-6: n[13] + Pij[13] >= 0
 apertura_5-6: - theta[4] + theta[5] + dtheta[14] = 0
 cap_sup_5-6: - 0.78 n[14] + Pij[14] <= 0
 cap_inf_5-6: 0.78 n[14] + Pij[14] >= 0
 balance_1: Pij[0] + Pij[1] + Pij[2] + Pij[3] + Pij[4] + Pa[0] + Pa[1]
   + Pa[2] = -0.3
 balance_2: - Pij[0] + Pij[5] + Pij[6] + Pij[7] + Pij[8] - Pa[0] + Pa[3]
   + Pa[4] = -2.4
 balance_3: - Pij[1] - Pij[5] + Pij[9] + Pij[10] + Pij[11] - Pa[3] + Pa[5]
   = 1.25
 balance_4: - Pij[2] - Pij[6] - Pij[9] + Pij[12] + Pij[13] - Pa[1] - Pa[4]
   = -1.6
 balance_5: - Pij[3] - Pij[7] - Pij[10] - Pij[12] + Pij[14] - Pa[2] - Pa[5]
   = -2.4
 balance_6: - Pij[4] - Pij[8] - Pij[11] - Pij[13] - Pij[14] = 5.45
 bilineal_1-2: Pij[0] + [ - 2.5 n[0] * dtheta[0] ] = 0
 bilineal_1-3: Pij[1] + [ - 2.631578947368421 n[1] * dtheta[1] ] = 0
 bilineal_1-4: Pij[2] + [ - 1.666666666666667 n[2] * dtheta[2] ] = 0
 bilineal_1-5: Pij[3] + [ - 5 n[3] * dtheta[3] ] = 0
 bilineal_1-6: Pij[4] + [ - 1.470588235294118 n[4] * dtheta[4] ] = 0
 bilineal_2-3: Pij[5] + [ - 5 n[5] * dtheta[5] ] = 0
 bilineal_2-4: Pij[6] + [ - 2.5 n[6] * dtheta[6] ] = 0
 bilineal_2-5: Pij[7] + [ - 3.225806451612903 n[7] * dtheta[7] ] = 0
 bilineal_2-6: Pij[8] + [ - 3.333333333333333 n[8] * dtheta[8] ] = 0
 bilineal_3-4: Pij[9] + [ - 1.694915254237288 n[9] * dtheta[9] ] = 0
 bilineal_3-5: Pij[10] + [ - 5 n[10] * dtheta[10] ] = 0
 bilineal_3-6: Pij[11] + [ - 2.083333333333333 n[11] * dtheta[11] ] = 0
 bilineal_4-5: Pij[12] + [ - 1.587301587301587 n[12] * dtheta[12] ] = 0
 bilineal_4-6: Pij[13] + [ - 3.333333333333333 n[13] * dtheta[13] ] = 0
 bilineal_5-6: Pij[14] + [ - 1.639344262295082 n[14] * dtheta[14] ] = 0
Bounds
 -1.5708 <= theta[0] <= 1.5708
 -1.5708 <= theta[1] <= 1.5708
 -1.5708 <= theta[2] <= 1.5708
 -1.5708 <= theta[3] <= 1.5708
 theta[4] = 0
 -1.5708 <= theta[5] <= 1.5708
 n[0] <= 5
 n[1] <= 5
 n[2] <= 5
 n[3] <= 5
 n[4] <= 5
 n[5] <= 5
 n[6] <= 5
 n[7] <= 5
 n[8] <= 5
 n[9] <= 5
 n[10] <= 5
 n[11] <= 5
 n[12] <= 5
 n[13] <= 5
 n[14] <= 5
 -3.1416 <= dtheta[0] <= 3.1416
 -3.1416 <= dtheta[1] <= 3.1416
 -3.1416 <= dtheta[2] <= 3.1416
 -3.1416 <= dtheta[3] <= 3.1416
 -3.1416 <= dtheta[4] <= 3.1416
 -3.1416 <= dtheta[5] <= 3.1416
 -3.1416 <= dtheta[6] <= 3.1416
 -3.1416 <= dtheta[7] <= 3.1416
 -3.1416 <= dtheta[8] <= 3.1416
 -3.1416 <= dtheta[9] <= 3.1416
 -3.1416 <= dtheta[10] <= 3.1416
 -3.1416 <= dtheta[11] <= 3.1416
 -3.1416 <= dtheta[12] <= 3.1416
 -3.1416 <= dtheta[13] <= 3.1416
 -3.1416 <= dtheta[14] <= 3.1416
 -5 <= Pij[0] <= 5
 -5 <= Pij[1] <= 5
 -4 <= Pij[2] <= 4
 -5 <= Pij[3] <= 5
 -3.5 <= Pij[4] <= 3.5
 -5 <= Pij[5] <= 5
 -5 <= Pij[6] <= 5
 -5 <= Pij[7] <= 5
 -5 <= Pij[8] <= 5
 -4.1 <= Pij[9] <= 4.1
 -5 <= Pij[10] <= 5
 -5 <= Pij[11] <= 5
 -3.75 <= Pij[12] <= 3.75
 -5 <= Pij[13] <= 5
 -3.9 <= Pij[14] <= 3.9
 -1 <= Pa[0] <= 1
 -0.8 <= Pa[1] <= 0.8
 -1 <= Pa[2] <= 1
 -1 <= Pa[3] <= 1
 -1 <= Pa[4] <= 1
 -1 <= Pa[5] <= 1
Generals
 n[0] n[1] n[2] n[3] n[4] n[5] n[6] n[7] n[8] n[9] n[10] n[11] n[12] n[13]
 n[14]
End

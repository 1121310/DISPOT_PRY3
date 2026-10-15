\ Model TNEP_LP_Villasana_Garver
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xfdad0b10afc25067
Minimize
  0 theta[5] + 150 Pmas[0] + 150 Pmas[1] + 305 Pmas[2] + 100 Pmas[3]
   + 150 Pmenos[0] + 150 Pmenos[1] + 305 Pmenos[2] + 100 Pmenos[3]
Subject To
 KVL_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + PF[0] = 0
 KVL_1-4_1: - 1.666666666666667 theta[0] + 1.666666666666667 theta[3]
   + PF[1] = 0
 KVL_1-5_2: - 5 theta[0] + 5 theta[4] + PF[2] = 0
 KVL_2-3_3: - 5 theta[1] + 5 theta[2] + PF[3] = 0
 KVL_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + PF[4] = 0
 KVL_3-5_5: - 5 theta[2] + 5 theta[4] + PF[5] = 0
 balance_1: - PF[0] - PF[1] - PF[2] = 0.3
 balance_2: PF[0] - PF[3] - PF[4] + Pmas[0] - Pmenos[0] = 2.4
 balance_3: PF[3] - PF[5] - Pmas[3] + Pmenos[3] = -1.25
 balance_4: PF[1] + PF[4] + Pmas[1] - Pmenos[1] = 1.6
 balance_5: PF[2] + PF[5] + Pmas[2] + Pmas[3] - Pmenos[2] - Pmenos[3]
   = 2.4
 balance_6: - Pmas[0] - Pmas[1] - Pmas[2] + Pmenos[0] + Pmenos[1]
   + Pmenos[2] = -5.45
Bounds
 theta[0] free
 theta[1] free
 theta[2] free
 theta[3] free
 theta[4] = 0
 theta[5] = 0
 -1 <= PF[0] <= 1
 -0.8 <= PF[1] <= 0.8
 -1 <= PF[2] <= 1
 -1 <= PF[3] <= 1
 -1 <= PF[4] <= 1
 -1 <= PF[5] <= 1
End

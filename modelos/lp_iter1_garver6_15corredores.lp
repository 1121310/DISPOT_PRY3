\ Model TNEP_LP_Villasana_Garver
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x9ebf4abd1da557e6
Minimize
  0 theta[5] + 200 Pmas[0] + 190 Pmas[1] + 375 Pmas[2] + 100 Pmas[3]
   + 485.7142857142857 Pmas[4] + 100 Pmas[5] + 200 Pmas[6] + 155 Pmas[7]
   + 150 Pmas[8] + 359.7560975609756 Pmas[9] + 100 Pmas[10] + 240 Pmas[11]
   + 420 Pmas[12] + 150 Pmas[13] + 391.025641025641 Pmas[14]
   + 200 Pmenos[0] + 190 Pmenos[1] + 375 Pmenos[2] + 100 Pmenos[3]
   + 485.7142857142857 Pmenos[4] + 100 Pmenos[5] + 200 Pmenos[6]
   + 155 Pmenos[7] + 150 Pmenos[8] + 359.7560975609756 Pmenos[9]
   + 100 Pmenos[10] + 240 Pmenos[11] + 420 Pmenos[12] + 150 Pmenos[13]
   + 391.025641025641 Pmenos[14]
Subject To
 KVL_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + PF[0] = 0
 KVL_1-4_1: - 1.666666666666667 theta[0] + 1.666666666666667 theta[3]
   + PF[1] = 0
 KVL_1-5_2: - 5 theta[0] + 5 theta[4] + PF[2] = 0
 KVL_2-3_3: - 5 theta[1] + 5 theta[2] + PF[3] = 0
 KVL_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + PF[4] = 0
 KVL_3-5_5: - 5 theta[2] + 5 theta[4] + PF[5] = 0
 balance_1: - PF[0] - PF[1] - PF[2] - Pmas[0] - Pmas[1] - Pmas[2] - Pmas[3]
   - Pmas[4] + Pmenos[0] + Pmenos[1] + Pmenos[2] + Pmenos[3] + Pmenos[4]
   = 0.3
 balance_2: PF[0] - PF[3] - PF[4] + Pmas[0] - Pmas[5] - Pmas[6] - Pmas[7]
   - Pmas[8] - Pmenos[0] + Pmenos[5] + Pmenos[6] + Pmenos[7] + Pmenos[8]
   = 2.4
 balance_3: PF[3] - PF[5] + Pmas[1] + Pmas[5] - Pmas[9] - Pmas[10]
   - Pmas[11] - Pmenos[1] - Pmenos[5] + Pmenos[9] + Pmenos[10] + Pmenos[11]
   = -1.25
 balance_4: PF[1] + PF[4] + Pmas[2] + Pmas[6] + Pmas[9] - Pmas[12]
   - Pmas[13] - Pmenos[2] - Pmenos[6] - Pmenos[9] + Pmenos[12] + Pmenos[13]
   = 1.6
 balance_5: PF[2] + PF[5] + Pmas[3] + Pmas[7] + Pmas[10] + Pmas[12]
   - Pmas[14] - Pmenos[3] - Pmenos[7] - Pmenos[10] - Pmenos[12]
   + Pmenos[14] = 2.4
 balance_6: Pmas[4] + Pmas[8] + Pmas[11] + Pmas[13] + Pmas[14] - Pmenos[4]
   - Pmenos[8] - Pmenos[11] - Pmenos[13] - Pmenos[14] = -5.45
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

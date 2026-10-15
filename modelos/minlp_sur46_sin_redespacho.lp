\ Model TNEP_MINLP_bilineal
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x1315c309290dd33b
Minimize
  6.268 n[0] + 8.288 n[1] + 7.934 n[2] + 8.178 n[3] + 8.178 n[4]
   + 16.005 n[5] + 37.748 n[6] + 8.178 n[7] + 8.178 n[8] + 4.349 n[9]
   + 7.076 n[10] + 6.217 n[11] + 7.732 n[12] + 7.48 n[13] + 6.823 n[14]
   + 4.046 n[15] + 2.581 n[16] + 8.793 n[17] + 11.267 n[18] + 5.106 n[19]
   + 9.803 n[20] + 11.57 n[21] + 7.126 n[22] + 12.732 n[23] + 32.632 n[24]
   + 10.505 n[25] + 8.715 n[26] + 10.409 n[27] + 5.712 n[28] + 5.409 n[29]
   + 5.308 n[30] + 5.662 n[31] + 10.611 n[32] + 9.399 n[33] + 6.167 n[34]
   + 13.237 n[35] + 7.025 n[36] + 3.591 n[37] + 12.631 n[38] + 2.329 n[39]
   + 8.389 n[40] + 13.388 n[41] + 12.934 n[42] + 6.268 n[43] + 6.116 n[44]
   + 35.957 n[45] + 11.924 n[46] + 23.423 n[47] + 26.365 n[48]
   + 24.319 n[49] + 8.178 n[50] + 5.965 n[51] + 2.884 n[52] + 10.889 n[53]
   + 14.247 n[54] + 6.167 n[55] + 24.319 n[56] + 26.365 n[57]
   + 36.213 n[58] + 27.516 n[59] + 21.121 n[60] + 37.109 n[61]
   + 7.052 n[62] + 7.819 n[63] + 8.331 n[64] + 6.672 n[65] + 3.894 n[66]
   + 39.283 n[67] + 46.701 n[68] + 32.632 n[69] + 35.957 n[70]
   + 17.284 n[71] + 13.994 n[72] + 8.178 n[73] + 8.178 n[74] + 8.178 n[75]
   + 8.178 n[76] + 8.178 n[77] + 8.178 n[78]
Subject To
 flujo_existente_1-7_0: - 16.23376623376623 theta[0]
   + 16.23376623376623 theta[6] + Pa[0] = 0
 flujo_existente_1-2_1: - 18.7793427230047 theta[0]
   + 18.7793427230047 theta[1] + Pa[1] = 0
 flujo_existente_4-9_2: - 10.82251082251082 theta[3]
   + 10.82251082251082 theta[8] + Pa[2] = 0
 flujo_existente_5-9_3: - 8.525149190110827 theta[4]
   + 8.525149190110827 theta[8] + Pa[3] = 0
 flujo_existente_5-8_4: - 8.8339222614841 theta[4]
   + 8.8339222614841 theta[7] + Pa[4] = 0
 flujo_existente_7-8_5: - 9.775171065493646 theta[6]
   + 9.775171065493646 theta[7] + Pa[5] = 0
 flujo_existente_4-5_6: - 35.3356890459364 theta[3]
   + 35.3356890459364 theta[4] + Pa[6] = 0
 flujo_existente_2-5_7: - 61.7283950617284 theta[1]
   + 61.7283950617284 theta[4] + Pa[7] = 0
 flujo_existente_8-13_8: - 7.41839762611276 theta[7]
   + 7.41839762611276 theta[12] + Pa[8] = 0
 flujo_existente_9-14_9: - 11.38952164009112 theta[8]
   + 11.38952164009112 theta[13] + Pa[9] = 0
 flujo_existente_12-14_10: - 27.02702702702703 theta[11]
   + 27.02702702702703 theta[13] + Pa[10] = 0
 flujo_existente_14-18_11: - 13.21003963011889 theta[13]
   + 13.21003963011889 theta[17] + Pa[11] = 0
 flujo_existente_13-18_12: - 5.54016620498615 theta[12]
   + 5.54016620498615 theta[17] + Pa[12] = 0
 flujo_existente_13-20_13: - 9.319664492078285 theta[12]
   + 9.319664492078285 theta[19] + Pa[13] = 0
 flujo_existente_18-20_14: - 5.007511266900351 theta[17]
   + 5.007511266900351 theta[19] + Pa[14] = 0
 flujo_existente_19-21_15: - 35.97122302158274 theta[18]
   + 35.97122302158274 theta[20] + Pa[15] = 0
 flujo_existente_16-17_16: - 128.2051282051282 theta[15]
   + 128.2051282051282 theta[16] + Pa[16] = 0
 flujo_existente_17-19_17: - 163.9344262295082 theta[16]
   + 163.9344262295082 theta[18] + Pa[17] = 0
 flujo_existente_14-26_18: - 6.195786864931847 theta[13]
   + 6.195786864931847 theta[25] + Pa[18] = 0
 flujo_existente_14-22_19: - 11.9047619047619 theta[13]
   + 11.9047619047619 theta[21] + Pa[19] = 0
 flujo_existente_22-26_20: - 12.65822784810127 theta[21]
   + 12.65822784810127 theta[25] + Pa[20] = 0
 flujo_existente_20-23_21: - 21.45922746781116 theta[19]
   + 21.45922746781116 theta[22] + Pa[21] = 0
 flujo_existente_23-24_22: - 25.83979328165375 theta[22]
   + 25.83979328165375 theta[23] + Pa[22] = 0
 flujo_existente_26-27_23: - 24.03846153846154 theta[25]
   + 24.03846153846154 theta[26] + Pa[23] = 0
 flujo_existente_24-34_24: - 6.07164541590771 theta[23]
   + 6.07164541590771 theta[33] + Pa[24] = 0
 flujo_existente_24-33_25: - 6.906077348066297 theta[23]
   + 6.906077348066297 theta[32] + Pa[25] = 0
 flujo_existente_33-34_26: - 7.905138339920948 theta[32]
   + 7.905138339920948 theta[33] + Pa[26] = 0
 flujo_existente_27-36_27: - 10.92896174863388 theta[26]
   + 10.92896174863388 theta[35] + Pa[27] = 0
 flujo_existente_27-38_28: - 9.615384615384615 theta[26]
   + 9.615384615384615 theta[37] + Pa[28] = 0
 flujo_existente_36-37_29: - 9.460737937559129 theta[35]
   + 9.460737937559129 theta[36] + Pa[29] = 0
 flujo_existente_34-35_30: - 40.73319755600815 theta[33]
   + 40.73319755600815 theta[34] + Pa[30] = 0
 flujo_existente_35-38_31: - 5.05050505050505 theta[34]
   + 5.05050505050505 theta[37] + Pa[31] = 0
 flujo_existente_37-39_32: - 35.3356890459364 theta[36]
   + 35.3356890459364 theta[38] + Pa[32] = 0
 flujo_existente_37-40_33: - 7.806401249024201 theta[36]
   + 7.806401249024201 theta[39] + Pa[33] = 0
 flujo_existente_37-42_34: - 4.750593824228028 theta[36]
   + 4.750593824228028 theta[41] + Pa[34] = 0
 flujo_existente_39-42_35: - 14.77832512315271 theta[38]
   + 14.77832512315271 theta[41] + Pa[35] = 0
 flujo_existente_40-42_36: - 10.72961373390558 theta[39]
   + 10.72961373390558 theta[41] + Pa[36] = 0
 flujo_existente_38-42_37: - 33.0760749724366 theta[37]
   + 33.0760749724366 theta[41] + Pa[37] = 0
 flujo_existente_32-43_38: - 32.36245954692556 theta[31]
   + 32.36245954692556 theta[42] + Pa[38] = 0
 flujo_existente_42-44_39: - 8.291873963515755 theta[41]
   + 8.291873963515755 theta[43] + Pa[39] = 0
 flujo_existente_44-45_40: - 5.364806866952789 theta[43]
   + 5.364806866952789 theta[44] + Pa[40] = 0
 flujo_existente_19-32_41: - 51.28205128205128 theta[18]
   + 51.28205128205128 theta[31] + Pa[41] = 0
 flujo_existente_46-19_42: 45.04504504504504 theta[18]
   - 45.04504504504504 theta[45] + Pa[42] = 0
 flujo_existente_46-16_43: 49.26108374384237 theta[15]
   - 49.26108374384237 theta[45] + Pa[43] = 0
 flujo_existente_18-19_44: - 80 theta[17] + 80 theta[18] + Pa[44] = 0
 flujo_existente_20-21_45: - 80 theta[19] + 80 theta[20] + Pa[45] = 0
 flujo_existente_42-43_46: - 80 theta[41] + 80 theta[42] + Pa[46] = 0
 apertura_20-23: - theta[19] + theta[22] + dtheta[0] = 0
 cap_sup_20-23: - 2.7 n[0] + Pij[0] <= 0
 cap_inf_20-23: 2.7 n[0] + Pij[0] >= 0
 apertura_33-34: - theta[32] + theta[33] + dtheta[1] = 0
 cap_sup_33-34: - 2.7 n[1] + Pij[1] <= 0
 cap_inf_33-34: 2.7 n[1] + Pij[1] >= 0
 apertura_42-44: - theta[41] + theta[43] + dtheta[2] = 0
 cap_sup_42-44: - 2.7 n[2] + Pij[2] <= 0
 cap_inf_42-44: 2.7 n[2] + Pij[2] >= 0
 apertura_20-21: - theta[19] + theta[20] + dtheta[3] = 0
 cap_sup_20-21: - 6 n[3] + Pij[3] <= 0
 cap_inf_20-21: 6 n[3] + Pij[3] >= 0
 apertura_42-43: - theta[41] + theta[42] + dtheta[4] = 0
 cap_sup_42-43: - 6 n[4] + Pij[4] <= 0
 cap_inf_42-43: 6 n[4] + Pij[4] >= 0
 apertura_46-6: theta[5] - theta[45] + dtheta[5] = 0
 cap_sup_46-6: - 20 n[5] + Pij[5] <= 0
 cap_inf_46-6: 20 n[5] + Pij[5] >= 0
 apertura_19-25: - theta[18] + theta[24] + dtheta[6] = 0
 cap_sup_19-25: - 14 n[6] + Pij[6] <= 0
 cap_inf_19-25: 14 n[6] + Pij[6] >= 0
 apertura_24-25: - theta[23] + theta[24] + dtheta[7] = 0
 cap_sup_24-25: - 6 n[7] + Pij[7] <= 0
 cap_inf_24-25: 6 n[7] + Pij[7] >= 0
 apertura_5-6: - theta[4] + theta[5] + dtheta[8] = 0
 cap_sup_5-6: - 6 n[8] + Pij[8] <= 0
 cap_inf_5-6: 6 n[8] + Pij[8] >= 0
 apertura_1-7: - theta[0] + theta[6] + dtheta[9] = 0
 cap_sup_1-7: - 2.7 n[9] + Pij[9] <= 0
 cap_inf_1-7: 2.7 n[9] + Pij[9] >= 0
 apertura_1-2: - theta[0] + theta[1] + dtheta[10] = 0
 cap_sup_1-2: - 2.7 n[10] + Pij[10] <= 0
 cap_inf_1-2: 2.7 n[10] + Pij[10] >= 0
 apertura_4-9: - theta[3] + theta[8] + dtheta[11] = 0
 cap_sup_4-9: - 2.7 n[11] + Pij[11] <= 0
 cap_inf_4-9: 2.7 n[11] + Pij[11] >= 0
 apertura_5-9: - theta[4] + theta[8] + dtheta[12] = 0
 cap_sup_5-9: - 2.7 n[12] + Pij[12] <= 0
 cap_inf_5-9: 2.7 n[12] + Pij[12] >= 0
 apertura_5-8: - theta[4] + theta[7] + dtheta[13] = 0
 cap_sup_5-8: - 2.7 n[13] + Pij[13] <= 0
 cap_inf_5-8: 2.7 n[13] + Pij[13] >= 0
 apertura_7-8: - theta[6] + theta[7] + dtheta[14] = 0
 cap_sup_7-8: - 2.7 n[14] + Pij[14] <= 0
 cap_inf_7-8: 2.7 n[14] + Pij[14] >= 0
 apertura_4-5: - theta[3] + theta[4] + dtheta[15] = 0
 cap_sup_4-5: - 2.7 n[15] + Pij[15] <= 0
 cap_inf_4-5: 2.7 n[15] + Pij[15] >= 0
 apertura_2-5: - theta[1] + theta[4] + dtheta[16] = 0
 cap_sup_2-5: - 2.7 n[16] + Pij[16] <= 0
 cap_inf_2-5: 2.7 n[16] + Pij[16] >= 0
 apertura_8-13: - theta[7] + theta[12] + dtheta[17] = 0
 cap_sup_8-13: - 2.4 n[17] + Pij[17] <= 0
 cap_inf_8-13: 2.4 n[17] + Pij[17] >= 0
 apertura_9-14: - theta[8] + theta[13] + dtheta[18] = 0
 cap_sup_9-14: - 2.2 n[18] + Pij[18] <= 0
 cap_inf_9-14: 2.2 n[18] + Pij[18] >= 0
 apertura_12-14: - theta[11] + theta[13] + dtheta[19] = 0
 cap_sup_12-14: - 2.7 n[19] + Pij[19] <= 0
 cap_inf_12-14: 2.7 n[19] + Pij[19] >= 0
 apertura_14-18: - theta[13] + theta[17] + dtheta[20] = 0
 cap_sup_14-18: - 2.4 n[20] + Pij[20] <= 0
 cap_inf_14-18: 2.4 n[20] + Pij[20] >= 0
 apertura_13-18: - theta[12] + theta[17] + dtheta[21] = 0
 cap_sup_13-18: - 2.2 n[21] + Pij[21] <= 0
 cap_inf_13-18: 2.2 n[21] + Pij[21] >= 0
 apertura_13-20: - theta[12] + theta[19] + dtheta[22] = 0
 cap_sup_13-20: - 2.7 n[22] + Pij[22] <= 0
 cap_inf_13-20: 2.7 n[22] + Pij[22] >= 0
 apertura_18-20: - theta[17] + theta[19] + dtheta[23] = 0
 cap_sup_18-20: - 2 n[23] + Pij[23] <= 0
 cap_inf_18-20: 2 n[23] + Pij[23] >= 0
 apertura_19-21: - theta[18] + theta[20] + dtheta[24] = 0
 cap_sup_19-21: - 15 n[24] + Pij[24] <= 0
 cap_inf_19-21: 15 n[24] + Pij[24] >= 0
 apertura_16-17: - theta[15] + theta[16] + dtheta[25] = 0
 cap_sup_16-17: - 20 n[25] + Pij[25] <= 0
 cap_inf_16-17: 20 n[25] + Pij[25] >= 0
 apertura_17-19: - theta[16] + theta[18] + dtheta[26] = 0
 cap_sup_17-19: - 20 n[26] + Pij[26] <= 0
 cap_inf_17-19: 20 n[26] + Pij[26] >= 0
 apertura_14-26: - theta[13] + theta[25] + dtheta[27] = 0
 cap_sup_14-26: - 2.2 n[27] + Pij[27] <= 0
 cap_inf_14-26: 2.2 n[27] + Pij[27] >= 0
 apertura_14-22: - theta[13] + theta[21] + dtheta[28] = 0
 cap_sup_14-22: - 2.7 n[28] + Pij[28] <= 0
 cap_inf_14-22: 2.7 n[28] + Pij[28] >= 0
 apertura_22-26: - theta[21] + theta[25] + dtheta[29] = 0
 cap_sup_22-26: - 2.7 n[29] + Pij[29] <= 0
 cap_inf_22-26: 2.7 n[29] + Pij[29] >= 0
 apertura_23-24: - theta[22] + theta[23] + dtheta[30] = 0
 cap_sup_23-24: - 2.7 n[30] + Pij[30] <= 0
 cap_inf_23-24: 2.7 n[30] + Pij[30] >= 0
 apertura_26-27: - theta[25] + theta[26] + dtheta[31] = 0
 cap_sup_26-27: - 2.7 n[31] + Pij[31] <= 0
 cap_inf_26-27: 2.7 n[31] + Pij[31] >= 0
 apertura_24-34: - theta[23] + theta[33] + dtheta[32] = 0
 cap_sup_24-34: - 2.2 n[32] + Pij[32] <= 0
 cap_inf_24-34: 2.2 n[32] + Pij[32] >= 0
 apertura_24-33: - theta[23] + theta[32] + dtheta[33] = 0
 cap_sup_24-33: - 2.4 n[33] + Pij[33] <= 0
 cap_inf_24-33: 2.4 n[33] + Pij[33] >= 0
 apertura_27-36: - theta[26] + theta[35] + dtheta[34] = 0
 cap_sup_27-36: - 2.7 n[34] + Pij[34] <= 0
 cap_inf_27-36: 2.7 n[34] + Pij[34] >= 0
 apertura_27-38: - theta[26] + theta[37] + dtheta[35] = 0
 cap_sup_27-38: - 2 n[35] + Pij[35] <= 0
 cap_inf_27-38: 2 n[35] + Pij[35] >= 0
 apertura_36-37: - theta[35] + theta[36] + dtheta[36] = 0
 cap_sup_36-37: - 2.7 n[36] + Pij[36] <= 0
 cap_inf_36-37: 2.7 n[36] + Pij[36] >= 0
 apertura_34-35: - theta[33] + theta[34] + dtheta[37] = 0
 cap_sup_34-35: - 2.7 n[37] + Pij[37] <= 0
 cap_inf_34-35: 2.7 n[37] + Pij[37] >= 0
 apertura_35-38: - theta[34] + theta[37] + dtheta[38] = 0
 cap_sup_35-38: - 2 n[38] + Pij[38] <= 0
 cap_inf_35-38: 2 n[38] + Pij[38] >= 0
 apertura_37-39: - theta[36] + theta[38] + dtheta[39] = 0
 cap_sup_37-39: - 2.7 n[39] + Pij[39] <= 0
 cap_inf_37-39: 2.7 n[39] + Pij[39] >= 0
 apertura_37-40: - theta[36] + theta[39] + dtheta[40] = 0
 cap_sup_37-40: - 2.7 n[40] + Pij[40] <= 0
 cap_inf_37-40: 2.7 n[40] + Pij[40] >= 0
 apertura_37-42: - theta[36] + theta[41] + dtheta[41] = 0
 cap_sup_37-42: - 2 n[41] + Pij[41] <= 0
 cap_inf_37-42: 2 n[41] + Pij[41] >= 0
 apertura_39-42: - theta[38] + theta[41] + dtheta[42] = 0
 cap_sup_39-42: - 2 n[42] + Pij[42] <= 0
 cap_inf_39-42: 2 n[42] + Pij[42] >= 0
 apertura_40-42: - theta[39] + theta[41] + dtheta[43] = 0
 cap_sup_40-42: - 2.7 n[43] + Pij[43] <= 0
 cap_inf_40-42: 2.7 n[43] + Pij[43] >= 0
 apertura_38-42: - theta[37] + theta[41] + dtheta[44] = 0
 cap_sup_38-42: - 2.7 n[44] + Pij[44] <= 0
 cap_inf_38-42: 2.7 n[44] + Pij[44] >= 0
 apertura_32-43: - theta[31] + theta[42] + dtheta[45] = 0
 cap_sup_32-43: - 14 n[45] + Pij[45] <= 0
 cap_inf_32-43: 14 n[45] + Pij[45] >= 0
 apertura_44-45: - theta[43] + theta[44] + dtheta[46] = 0
 cap_sup_44-45: - 2 n[46] + Pij[46] <= 0
 cap_inf_44-45: 2 n[46] + Pij[46] >= 0
 apertura_19-32: - theta[18] + theta[31] + dtheta[47] = 0
 cap_sup_19-32: - 18 n[47] + Pij[47] <= 0
 cap_inf_19-32: 18 n[47] + Pij[47] >= 0
 apertura_46-19: theta[18] - theta[45] + dtheta[48] = 0
 cap_sup_46-19: - 18 n[48] + Pij[48] <= 0
 cap_inf_46-19: 18 n[48] + Pij[48] >= 0
 apertura_46-16: theta[15] - theta[45] + dtheta[49] = 0
 cap_sup_46-16: - 18 n[49] + Pij[49] <= 0
 cap_inf_46-16: 18 n[49] + Pij[49] >= 0
 apertura_18-19: - theta[17] + theta[18] + dtheta[50] = 0
 cap_sup_18-19: - 6 n[50] + Pij[50] <= 0
 cap_inf_18-19: 6 n[50] + Pij[50] >= 0
 apertura_2-4: - theta[1] + theta[3] + dtheta[51] = 0
 cap_sup_2-4: - 2.7 n[51] + Pij[51] <= 0
 cap_inf_2-4: 2.7 n[51] + Pij[51] >= 0
 apertura_14-15: - theta[13] + theta[14] + dtheta[52] = 0
 cap_sup_14-15: - 2.7 n[52] + Pij[52] <= 0
 cap_inf_14-15: 2.7 n[52] + Pij[52] >= 0
 apertura_46-10: theta[9] - theta[45] + dtheta[53] = 0
 cap_sup_46-10: - 20 n[53] + Pij[53] <= 0
 cap_inf_46-10: 20 n[53] + Pij[53] >= 0
 apertura_4-11: - theta[3] + theta[10] + dtheta[54] = 0
 cap_sup_4-11: - 2.4 n[54] + Pij[54] <= 0
 cap_inf_4-11: 2.4 n[54] + Pij[54] >= 0
 apertura_5-11: - theta[4] + theta[10] + dtheta[55] = 0
 cap_sup_5-11: - 2.7 n[55] + Pij[55] <= 0
 cap_inf_5-11: 2.7 n[55] + Pij[55] >= 0
 apertura_46-3: theta[2] - theta[45] + dtheta[56] = 0
 cap_sup_46-3: - 18 n[56] + Pij[56] <= 0
 cap_inf_46-3: 18 n[56] + Pij[56] >= 0
 apertura_16-28: - theta[15] + theta[27] + dtheta[57] = 0
 cap_sup_16-28: - 18 n[57] + Pij[57] <= 0
 cap_inf_16-28: 18 n[57] + Pij[57] >= 0
 apertura_16-32: - theta[15] + theta[31] + dtheta[58] = 0
 cap_sup_16-32: - 14 n[58] + Pij[58] <= 0
 cap_inf_16-32: 14 n[58] + Pij[58] >= 0
 apertura_17-32: - theta[16] + theta[31] + dtheta[59] = 0
 cap_sup_17-32: - 17 n[59] + Pij[59] <= 0
 cap_inf_17-32: 17 n[59] + Pij[59] >= 0
 apertura_21-25: - theta[20] + theta[24] + dtheta[60] = 0
 cap_sup_21-25: - 20 n[60] + Pij[60] <= 0
 cap_inf_21-25: 20 n[60] + Pij[60] >= 0
 apertura_25-32: - theta[24] + theta[31] + dtheta[61] = 0
 cap_sup_25-32: - 14 n[61] + Pij[61] <= 0
 cap_inf_25-32: 14 n[61] + Pij[61] >= 0
 apertura_31-32: - theta[30] + theta[31] + dtheta[62] = 0
 cap_sup_31-32: - 20 n[62] + Pij[62] <= 0
 cap_inf_31-32: 20 n[62] + Pij[62] >= 0
 apertura_28-31: - theta[27] + theta[30] + dtheta[63] = 0
 cap_sup_28-31: - 20 n[63] + Pij[63] <= 0
 cap_inf_28-31: 20 n[63] + Pij[63] >= 0
 apertura_28-30: - theta[27] + theta[29] + dtheta[64] = 0
 cap_sup_28-30: - 20 n[64] + Pij[64] <= 0
 cap_inf_28-30: 20 n[64] + Pij[64] >= 0
 apertura_27-29: - theta[26] + theta[28] + dtheta[65] = 0
 cap_sup_27-29: - 2.7 n[65] + Pij[65] <= 0
 cap_inf_27-29: 2.7 n[65] + Pij[65] >= 0
 apertura_26-29: - theta[25] + theta[28] + dtheta[66] = 0
 cap_sup_26-29: - 2.7 n[66] + Pij[66] <= 0
 cap_inf_26-29: 2.7 n[66] + Pij[66] >= 0
 apertura_28-41: - theta[27] + theta[40] + dtheta[67] = 0
 cap_sup_28-41: - 13 n[67] + Pij[67] <= 0
 cap_inf_28-41: 13 n[67] + Pij[67] >= 0
 apertura_28-43: - theta[27] + theta[42] + dtheta[68] = 0
 cap_sup_28-43: - 12 n[68] + Pij[68] <= 0
 cap_inf_28-43: 12 n[68] + Pij[68] >= 0
 apertura_31-41: - theta[30] + theta[40] + dtheta[69] = 0
 cap_sup_31-41: - 15 n[69] + Pij[69] <= 0
 cap_inf_31-41: 15 n[69] + Pij[69] >= 0
 apertura_32-41: - theta[31] + theta[40] + dtheta[70] = 0
 cap_sup_32-41: - 14 n[70] + Pij[70] <= 0
 cap_inf_32-41: 14 n[70] + Pij[70] >= 0
 apertura_41-43: - theta[40] + theta[42] + dtheta[71] = 0
 cap_sup_41-43: - 20 n[71] + Pij[71] <= 0
 cap_inf_41-43: 20 n[71] + Pij[71] >= 0
 apertura_40-45: - theta[39] + theta[44] + dtheta[72] = 0
 cap_sup_40-45: - 1.8 n[72] + Pij[72] <= 0
 cap_inf_40-45: 1.8 n[72] + Pij[72] >= 0
 apertura_15-16: - theta[14] + theta[15] + dtheta[73] = 0
 cap_sup_15-16: - 6 n[73] + Pij[73] <= 0
 cap_inf_15-16: 6 n[73] + Pij[73] >= 0
 apertura_46-11: theta[10] - theta[45] + dtheta[74] = 0
 cap_sup_46-11: - 6 n[74] + Pij[74] <= 0
 cap_inf_46-11: 6 n[74] + Pij[74] >= 0
 apertura_29-30: - theta[28] + theta[29] + dtheta[75] = 0
 cap_sup_29-30: - 6 n[75] + Pij[75] <= 0
 cap_inf_29-30: 6 n[75] + Pij[75] >= 0
 apertura_40-41: - theta[39] + theta[40] + dtheta[76] = 0
 cap_sup_40-41: - 6 n[76] + Pij[76] <= 0
 cap_inf_40-41: 6 n[76] + Pij[76] >= 0
 apertura_2-3: - theta[1] + theta[2] + dtheta[77] = 0
 cap_sup_2-3: - 6 n[77] + Pij[77] <= 0
 cap_inf_2-3: 6 n[77] + Pij[77] >= 0
 apertura_9-10: - theta[8] + theta[9] + dtheta[78] = 0
 cap_sup_9-10: - 6 n[78] + Pij[78] <= 0
 cap_inf_9-10: 6 n[78] + Pij[78] >= 0
 balance_1: Pij[9] + Pij[10] + Pa[0] + Pa[1] = 0
 balance_2: - Pij[10] + Pij[16] + Pij[51] + Pij[77] - Pa[1] + Pa[7]
   = -4.431
 balance_3: - Pij[56] - Pij[77] = 0
 balance_4: Pij[11] + Pij[15] - Pij[51] + Pij[54] + Pa[2] + Pa[6] = -3.007
 balance_5: Pij[8] + Pij[12] + Pij[13] - Pij[15] - Pij[16] + Pij[55]
   + Pa[3] + Pa[4] - Pa[6] - Pa[7] = -2.38
 balance_6: - Pij[5] - Pij[8] = 0
 balance_7: - Pij[9] + Pij[14] - Pa[0] + Pa[5] = 0
 balance_8: - Pij[13] - Pij[14] + Pij[17] - Pa[4] - Pa[5] + Pa[8] = -0.722
 balance_9: - Pij[11] - Pij[12] + Pij[18] + Pij[78] - Pa[2] - Pa[3] + Pa[9]
   = 0
 balance_10: - Pij[53] - Pij[78] = 0
 balance_11: - Pij[54] - Pij[55] - Pij[74] = 0
 balance_12: Pij[19] + Pa[10] = -5.119
 balance_13: - Pij[17] + Pij[21] + Pij[22] - Pa[8] + Pa[12] + Pa[13]
   = -1.858
 balance_14: - Pij[18] - Pij[19] + Pij[20] + Pij[27] + Pij[28] + Pij[52]
   - Pa[9] - Pa[10] + Pa[11] + Pa[18] + Pa[19] = 9.44
 balance_15: - Pij[52] + Pij[73] = 0
 balance_16: Pij[25] - Pij[49] + Pij[57] + Pij[58] - Pij[73] + Pa[16]
   - Pa[43] = 13.66
 balance_17: - Pij[25] + Pij[26] + Pij[59] - Pa[16] + Pa[17] = 10
 balance_18: - Pij[20] - Pij[21] + Pij[23] + Pij[50] - Pa[11] - Pa[12]
   + Pa[14] + Pa[44] = 0
 balance_19: Pij[6] + Pij[24] - Pij[26] + Pij[47] - Pij[48] - Pij[50]
   + Pa[15] - Pa[17] + Pa[41] - Pa[42] - Pa[44] = 7.73
 balance_20: Pij[0] + Pij[3] - Pij[22] - Pij[23] - Pa[13] - Pa[14] + Pa[21]
   + Pa[45] = -10.912
 balance_21: - Pij[3] - Pij[24] + Pij[60] - Pa[15] - Pa[45] = 0
 balance_22: - Pij[28] + Pij[29] - Pa[19] + Pa[20] = -0.819
 balance_23: - Pij[0] + Pij[30] - Pa[21] + Pa[22] = -4.581
 balance_24: Pij[7] - Pij[30] + Pij[32] + Pij[33] - Pa[22] + Pa[24]
   + Pa[25] = -4.782
 balance_25: - Pij[6] - Pij[7] - Pij[60] + Pij[61] = 0
 balance_26: - Pij[27] - Pij[29] + Pij[31] + Pij[66] - Pa[18] - Pa[20]
   + Pa[23] = -2.319
 balance_27: - Pij[31] + Pij[34] + Pij[35] + Pij[65] - Pa[23] + Pa[27]
   + Pa[28] = 0.54
 balance_28: - Pij[57] + Pij[63] + Pij[64] + Pij[67] + Pij[68] = 7.3
 balance_29: - Pij[65] - Pij[66] + Pij[75] = 0
 balance_30: - Pij[64] - Pij[75] = 0
 balance_31: Pij[62] - Pij[63] + Pij[69] = 3.1
 balance_32: Pij[45] - Pij[47] - Pij[58] - Pij[59] - Pij[61] - Pij[62]
   + Pij[70] + Pa[38] - Pa[41] = 4.5
 balance_33: Pij[1] - Pij[33] - Pa[25] + Pa[26] = -2.291
 balance_34: - Pij[1] - Pij[32] + Pij[37] - Pa[24] - Pa[26] + Pa[30]
   = 2.21
 balance_35: - Pij[37] + Pij[38] - Pa[30] + Pa[31] = -2.16
 balance_36: - Pij[34] + Pij[36] - Pa[27] + Pa[29] = -0.901
 balance_37: - Pij[36] + Pij[39] + Pij[40] + Pij[41] - Pa[29] + Pa[32]
   + Pa[33] + Pa[34] = 2.12
 balance_38: - Pij[35] - Pij[38] + Pij[44] - Pa[28] - Pa[31] + Pa[37]
   = -2.16
 balance_39: - Pij[39] + Pij[42] - Pa[32] + Pa[35] = 2.21
 balance_40: - Pij[40] + Pij[43] + Pij[72] + Pij[76] - Pa[33] + Pa[36]
   = -2.621
 balance_41: - Pij[67] - Pij[69] - Pij[70] + Pij[71] - Pij[76] = 0
 balance_42: Pij[2] + Pij[4] - Pij[41] - Pij[42] - Pij[43] - Pij[44]
   - Pa[34] - Pa[35] - Pa[36] - Pa[37] + Pa[39] + Pa[46] = -16.079
 balance_43: - Pij[4] - Pij[45] - Pij[68] - Pij[71] - Pa[38] - Pa[46] = 0
 balance_44: - Pij[2] + Pij[46] - Pa[39] + Pa[40] = -0.791
 balance_45: - Pij[46] - Pij[72] - Pa[40] = -0.867
 balance_46: Pij[5] + Pij[48] + Pij[49] + Pij[53] + Pij[56] + Pij[74]
   + Pa[42] + Pa[43] = 5.99
 bilineal_20-23: Pij[0] + [ - 10.72961373390558 n[0] * dtheta[0] ] = 0
 bilineal_33-34: Pij[1] + [ - 7.905138339920948 n[1] * dtheta[1] ] = 0
 bilineal_42-44: Pij[2] + [ - 8.291873963515755 n[2] * dtheta[2] ] = 0
 bilineal_20-21: Pij[3] + [ - 80 n[3] * dtheta[3] ] = 0
 bilineal_42-43: Pij[4] + [ - 80 n[4] * dtheta[4] ] = 0
 bilineal_46-6: Pij[5] + [ - 78.125 n[5] * dtheta[5] ] = 0
 bilineal_19-25: Pij[6] + [ - 30.76923076923077 n[6] * dtheta[6] ] = 0
 bilineal_24-25: Pij[7] + [ - 80 n[7] * dtheta[7] ] = 0
 bilineal_5-6: Pij[8] + [ - 80 n[8] * dtheta[8] ] = 0
 bilineal_1-7: Pij[9] + [ - 16.23376623376623 n[9] * dtheta[9] ] = 0
 bilineal_1-2: Pij[10] + [ - 9.389671361502348 n[10] * dtheta[10] ] = 0
 bilineal_4-9: Pij[11] + [ - 10.82251082251082 n[11] * dtheta[11] ] = 0
 bilineal_5-9: Pij[12] + [ - 8.525149190110827 n[12] * dtheta[12] ] = 0
 bilineal_5-8: Pij[13] + [ - 8.8339222614841 n[13] * dtheta[13] ] = 0
 bilineal_7-8: Pij[14] + [ - 9.775171065493646 n[14] * dtheta[14] ] = 0
 bilineal_4-5: Pij[15] + [ - 17.6678445229682 n[15] * dtheta[15] ] = 0
 bilineal_2-5: Pij[16] + [ - 30.8641975308642 n[16] * dtheta[16] ] = 0
 bilineal_8-13: Pij[17] + [ - 7.41839762611276 n[17] * dtheta[17] ] = 0
 bilineal_9-14: Pij[18] + [ - 5.694760820045558 n[18] * dtheta[18] ] = 0
 bilineal_12-14: Pij[19] + [ - 13.51351351351351 n[19] * dtheta[19] ] = 0
 bilineal_14-18: Pij[20] + [ - 6.605019815059445 n[20] * dtheta[20] ] = 0
 bilineal_13-18: Pij[21] + [ - 5.54016620498615 n[21] * dtheta[21] ] = 0
 bilineal_13-20: Pij[22] + [ - 9.319664492078285 n[22] * dtheta[22] ] = 0
 bilineal_18-20: Pij[23] + [ - 5.007511266900351 n[23] * dtheta[23] ] = 0
 bilineal_19-21: Pij[24] + [ - 35.97122302158274 n[24] * dtheta[24] ] = 0
 bilineal_16-17: Pij[25] + [ - 128.2051282051282 n[25] * dtheta[25] ] = 0
 bilineal_17-19: Pij[26] + [ - 163.9344262295082 n[26] * dtheta[26] ] = 0
 bilineal_14-26: Pij[27] + [ - 6.195786864931847 n[27] * dtheta[27] ] = 0
 bilineal_14-22: Pij[28] + [ - 11.9047619047619 n[28] * dtheta[28] ] = 0
 bilineal_22-26: Pij[29] + [ - 12.65822784810127 n[29] * dtheta[29] ] = 0
 bilineal_23-24: Pij[30] + [ - 12.91989664082687 n[30] * dtheta[30] ] = 0
 bilineal_26-27: Pij[31] + [ - 12.01923076923077 n[31] * dtheta[31] ] = 0
 bilineal_24-34: Pij[32] + [ - 6.07164541590771 n[32] * dtheta[32] ] = 0
 bilineal_24-33: Pij[33] + [ - 6.906077348066297 n[33] * dtheta[33] ] = 0
 bilineal_27-36: Pij[34] + [ - 10.92896174863388 n[34] * dtheta[34] ] = 0
 bilineal_27-38: Pij[35] + [ - 4.807692307692307 n[35] * dtheta[35] ] = 0
 bilineal_36-37: Pij[36] + [ - 9.460737937559129 n[36] * dtheta[36] ] = 0
 bilineal_34-35: Pij[37] + [ - 20.36659877800408 n[37] * dtheta[37] ] = 0
 bilineal_35-38: Pij[38] + [ - 5.05050505050505 n[38] * dtheta[38] ] = 0
 bilineal_37-39: Pij[39] + [ - 35.3356890459364 n[39] * dtheta[39] ] = 0
 bilineal_37-40: Pij[40] + [ - 7.806401249024201 n[40] * dtheta[40] ] = 0
 bilineal_37-42: Pij[41] + [ - 4.750593824228028 n[41] * dtheta[41] ] = 0
 bilineal_39-42: Pij[42] + [ - 4.926108374384236 n[42] * dtheta[42] ] = 0
 bilineal_40-42: Pij[43] + [ - 10.72961373390558 n[43] * dtheta[43] ] = 0
 bilineal_38-42: Pij[44] + [ - 11.02535832414553 n[44] * dtheta[44] ] = 0
 bilineal_32-43: Pij[45] + [ - 32.36245954692556 n[45] * dtheta[45] ] = 0
 bilineal_44-45: Pij[46] + [ - 5.364806866952789 n[46] * dtheta[46] ] = 0
 bilineal_19-32: Pij[47] + [ - 51.28205128205128 n[47] * dtheta[47] ] = 0
 bilineal_46-19: Pij[48] + [ - 45.04504504504504 n[48] * dtheta[48] ] = 0
 bilineal_46-16: Pij[49] + [ - 49.26108374384237 n[49] * dtheta[49] ] = 0
 bilineal_18-19: Pij[50] + [ - 80 n[50] * dtheta[50] ] = 0
 bilineal_2-4: Pij[51] + [ - 11.33786848072562 n[51] * dtheta[51] ] = 0
 bilineal_14-15: Pij[52] + [ - 26.7379679144385 n[52] * dtheta[52] ] = 0
 bilineal_46-10: Pij[53] + [ - 123.4567901234568 n[53] * dtheta[53] ] = 0
 bilineal_4-11: Pij[54] + [ - 4.452359750667854 n[54] * dtheta[54] ] = 0
 bilineal_5-11: Pij[55] + [ - 10.92896174863388 n[55] * dtheta[55] ] = 0
 bilineal_46-3: Pij[56] + [ - 49.26108374384237 n[56] * dtheta[56] ] = 0
 bilineal_16-28: Pij[57] + [ - 45.04504504504504 n[57] * dtheta[57] ] = 0
 bilineal_16-32: Pij[58] + [ - 32.15434083601286 n[58] * dtheta[58] ] = 0
 bilineal_17-32: Pij[59] + [ - 43.10344827586207 n[59] * dtheta[59] ] = 0
 bilineal_21-25: Pij[60] + [ - 57.4712643678161 n[60] * dtheta[60] ] = 0
 bilineal_25-32: Pij[61] + [ - 31.34796238244514 n[61] * dtheta[61] ] = 0
 bilineal_31-32: Pij[62] + [ - 217.3913043478261 n[62] * dtheta[62] ] = 0
 bilineal_28-31: Pij[63] + [ - 188.6792452830189 n[63] * dtheta[63] ] = 0
 bilineal_28-30: Pij[64] + [ - 172.4137931034483 n[64] * dtheta[64] ] = 0
 bilineal_27-29: Pij[65] + [ - 10.02004008016032 n[65] * dtheta[65] ] = 0
 bilineal_26-29: Pij[66] + [ - 18.48428835489834 n[66] * dtheta[66] ] = 0
 bilineal_28-41: Pij[67] + [ - 29.49852507374631 n[67] * dtheta[67] ] = 0
 bilineal_28-43: Pij[68] + [ - 24.63054187192119 n[68] * dtheta[68] ] = 0
 bilineal_31-41: Pij[69] + [ - 35.97122302158274 n[69] * dtheta[69] ] = 0
 bilineal_32-41: Pij[70] + [ - 32.36245954692556 n[70] * dtheta[70] ] = 0
 bilineal_41-43: Pij[71] + [ - 71.94244604316548 n[71] * dtheta[71] ] = 0
 bilineal_40-45: Pij[72] + [ - 4.535147392290249 n[72] * dtheta[72] ] = 0
 bilineal_15-16: Pij[73] + [ - 80 n[73] * dtheta[73] ] = 0
 bilineal_46-11: Pij[74] + [ - 80 n[74] * dtheta[74] ] = 0
 bilineal_29-30: Pij[75] + [ - 80 n[75] * dtheta[75] ] = 0
 bilineal_40-41: Pij[76] + [ - 80 n[76] * dtheta[76] ] = 0
 bilineal_2-3: Pij[77] + [ - 80 n[77] * dtheta[77] ] = 0
 bilineal_9-10: Pij[78] + [ - 80 n[78] * dtheta[78] ] = 0
Bounds
 -3.1416 <= theta[0] <= 3.1416
 -3.1416 <= theta[1] <= 3.1416
 -3.1416 <= theta[2] <= 3.1416
 -3.1416 <= theta[3] <= 3.1416
 -3.1416 <= theta[4] <= 3.1416
 -3.1416 <= theta[5] <= 3.1416
 -3.1416 <= theta[6] <= 3.1416
 -3.1416 <= theta[7] <= 3.1416
 -3.1416 <= theta[8] <= 3.1416
 -3.1416 <= theta[9] <= 3.1416
 -3.1416 <= theta[10] <= 3.1416
 -3.1416 <= theta[11] <= 3.1416
 -3.1416 <= theta[12] <= 3.1416
 -3.1416 <= theta[13] <= 3.1416
 -3.1416 <= theta[14] <= 3.1416
 theta[15] = 0
 -3.1416 <= theta[16] <= 3.1416
 -3.1416 <= theta[17] <= 3.1416
 -3.1416 <= theta[18] <= 3.1416
 -3.1416 <= theta[19] <= 3.1416
 -3.1416 <= theta[20] <= 3.1416
 -3.1416 <= theta[21] <= 3.1416
 -3.1416 <= theta[22] <= 3.1416
 -3.1416 <= theta[23] <= 3.1416
 -3.1416 <= theta[24] <= 3.1416
 -3.1416 <= theta[25] <= 3.1416
 -3.1416 <= theta[26] <= 3.1416
 -3.1416 <= theta[27] <= 3.1416
 -3.1416 <= theta[28] <= 3.1416
 -3.1416 <= theta[29] <= 3.1416
 -3.1416 <= theta[30] <= 3.1416
 -3.1416 <= theta[31] <= 3.1416
 -3.1416 <= theta[32] <= 3.1416
 -3.1416 <= theta[33] <= 3.1416
 -3.1416 <= theta[34] <= 3.1416
 -3.1416 <= theta[35] <= 3.1416
 -3.1416 <= theta[36] <= 3.1416
 -3.1416 <= theta[37] <= 3.1416
 -3.1416 <= theta[38] <= 3.1416
 -3.1416 <= theta[39] <= 3.1416
 -3.1416 <= theta[40] <= 3.1416
 -3.1416 <= theta[41] <= 3.1416
 -3.1416 <= theta[42] <= 3.1416
 -3.1416 <= theta[43] <= 3.1416
 -3.1416 <= theta[44] <= 3.1416
 -3.1416 <= theta[45] <= 3.1416
 n[0] <= 3
 n[1] <= 3
 n[2] <= 3
 n[3] <= 3
 n[4] <= 3
 n[5] <= 3
 n[6] <= 3
 n[7] <= 3
 n[8] <= 3
 n[9] <= 3
 n[10] <= 3
 n[11] <= 3
 n[12] <= 3
 n[13] <= 3
 n[14] <= 3
 n[15] <= 3
 n[16] <= 3
 n[17] <= 3
 n[18] <= 3
 n[19] <= 3
 n[20] <= 3
 n[21] <= 3
 n[22] <= 3
 n[23] <= 3
 n[24] <= 3
 n[25] <= 3
 n[26] <= 3
 n[27] <= 3
 n[28] <= 3
 n[29] <= 3
 n[30] <= 3
 n[31] <= 3
 n[32] <= 3
 n[33] <= 3
 n[34] <= 3
 n[35] <= 3
 n[36] <= 3
 n[37] <= 3
 n[38] <= 3
 n[39] <= 3
 n[40] <= 3
 n[41] <= 3
 n[42] <= 3
 n[43] <= 3
 n[44] <= 3
 n[45] <= 3
 n[46] <= 3
 n[47] <= 3
 n[48] <= 3
 n[49] <= 3
 n[50] <= 3
 n[51] <= 3
 n[52] <= 3
 n[53] <= 3
 n[54] <= 3
 n[55] <= 3
 n[56] <= 3
 n[57] <= 3
 n[58] <= 3
 n[59] <= 3
 n[60] <= 3
 n[61] <= 3
 n[62] <= 3
 n[63] <= 3
 n[64] <= 3
 n[65] <= 3
 n[66] <= 3
 n[67] <= 3
 n[68] <= 3
 n[69] <= 3
 n[70] <= 3
 n[71] <= 3
 n[72] <= 3
 n[73] <= 3
 n[74] <= 3
 n[75] <= 3
 n[76] <= 3
 n[77] <= 3
 n[78] <= 3
 -6.2832 <= dtheta[0] <= 6.2832
 -6.2832 <= dtheta[1] <= 6.2832
 -6.2832 <= dtheta[2] <= 6.2832
 -6.2832 <= dtheta[3] <= 6.2832
 -6.2832 <= dtheta[4] <= 6.2832
 -6.2832 <= dtheta[5] <= 6.2832
 -6.2832 <= dtheta[6] <= 6.2832
 -6.2832 <= dtheta[7] <= 6.2832
 -6.2832 <= dtheta[8] <= 6.2832
 -6.2832 <= dtheta[9] <= 6.2832
 -6.2832 <= dtheta[10] <= 6.2832
 -6.2832 <= dtheta[11] <= 6.2832
 -6.2832 <= dtheta[12] <= 6.2832
 -6.2832 <= dtheta[13] <= 6.2832
 -6.2832 <= dtheta[14] <= 6.2832
 -6.2832 <= dtheta[15] <= 6.2832
 -6.2832 <= dtheta[16] <= 6.2832
 -6.2832 <= dtheta[17] <= 6.2832
 -6.2832 <= dtheta[18] <= 6.2832
 -6.2832 <= dtheta[19] <= 6.2832
 -6.2832 <= dtheta[20] <= 6.2832
 -6.2832 <= dtheta[21] <= 6.2832
 -6.2832 <= dtheta[22] <= 6.2832
 -6.2832 <= dtheta[23] <= 6.2832
 -6.2832 <= dtheta[24] <= 6.2832
 -6.2832 <= dtheta[25] <= 6.2832
 -6.2832 <= dtheta[26] <= 6.2832
 -6.2832 <= dtheta[27] <= 6.2832
 -6.2832 <= dtheta[28] <= 6.2832
 -6.2832 <= dtheta[29] <= 6.2832
 -6.2832 <= dtheta[30] <= 6.2832
 -6.2832 <= dtheta[31] <= 6.2832
 -6.2832 <= dtheta[32] <= 6.2832
 -6.2832 <= dtheta[33] <= 6.2832
 -6.2832 <= dtheta[34] <= 6.2832
 -6.2832 <= dtheta[35] <= 6.2832
 -6.2832 <= dtheta[36] <= 6.2832
 -6.2832 <= dtheta[37] <= 6.2832
 -6.2832 <= dtheta[38] <= 6.2832
 -6.2832 <= dtheta[39] <= 6.2832
 -6.2832 <= dtheta[40] <= 6.2832
 -6.2832 <= dtheta[41] <= 6.2832
 -6.2832 <= dtheta[42] <= 6.2832
 -6.2832 <= dtheta[43] <= 6.2832
 -6.2832 <= dtheta[44] <= 6.2832
 -6.2832 <= dtheta[45] <= 6.2832
 -6.2832 <= dtheta[46] <= 6.2832
 -6.2832 <= dtheta[47] <= 6.2832
 -6.2832 <= dtheta[48] <= 6.2832
 -6.2832 <= dtheta[49] <= 6.2832
 -6.2832 <= dtheta[50] <= 6.2832
 -6.2832 <= dtheta[51] <= 6.2832
 -6.2832 <= dtheta[52] <= 6.2832
 -6.2832 <= dtheta[53] <= 6.2832
 -6.2832 <= dtheta[54] <= 6.2832
 -6.2832 <= dtheta[55] <= 6.2832
 -6.2832 <= dtheta[56] <= 6.2832
 -6.2832 <= dtheta[57] <= 6.2832
 -6.2832 <= dtheta[58] <= 6.2832
 -6.2832 <= dtheta[59] <= 6.2832
 -6.2832 <= dtheta[60] <= 6.2832
 -6.2832 <= dtheta[61] <= 6.2832
 -6.2832 <= dtheta[62] <= 6.2832
 -6.2832 <= dtheta[63] <= 6.2832
 -6.2832 <= dtheta[64] <= 6.2832
 -6.2832 <= dtheta[65] <= 6.2832
 -6.2832 <= dtheta[66] <= 6.2832
 -6.2832 <= dtheta[67] <= 6.2832
 -6.2832 <= dtheta[68] <= 6.2832
 -6.2832 <= dtheta[69] <= 6.2832
 -6.2832 <= dtheta[70] <= 6.2832
 -6.2832 <= dtheta[71] <= 6.2832
 -6.2832 <= dtheta[72] <= 6.2832
 -6.2832 <= dtheta[73] <= 6.2832
 -6.2832 <= dtheta[74] <= 6.2832
 -6.2832 <= dtheta[75] <= 6.2832
 -6.2832 <= dtheta[76] <= 6.2832
 -6.2832 <= dtheta[77] <= 6.2832
 -6.2832 <= dtheta[78] <= 6.2832
 -8.1 <= Pij[0] <= 8.1
 -8.1 <= Pij[1] <= 8.1
 -8.1 <= Pij[2] <= 8.1
 -18 <= Pij[3] <= 18
 -18 <= Pij[4] <= 18
 -60 <= Pij[5] <= 60
 -42 <= Pij[6] <= 42
 -18 <= Pij[7] <= 18
 -18 <= Pij[8] <= 18
 -8.1 <= Pij[9] <= 8.1
 -8.1 <= Pij[10] <= 8.1
 -8.1 <= Pij[11] <= 8.1
 -8.1 <= Pij[12] <= 8.1
 -8.1 <= Pij[13] <= 8.1
 -8.1 <= Pij[14] <= 8.1
 -8.1 <= Pij[15] <= 8.1
 -8.1 <= Pij[16] <= 8.1
 -7.2 <= Pij[17] <= 7.2
 -6.6 <= Pij[18] <= 6.6
 -8.1 <= Pij[19] <= 8.1
 -7.2 <= Pij[20] <= 7.2
 -6.6 <= Pij[21] <= 6.6
 -8.1 <= Pij[22] <= 8.1
 -6 <= Pij[23] <= 6
 -45 <= Pij[24] <= 45
 -60 <= Pij[25] <= 60
 -60 <= Pij[26] <= 60
 -6.6 <= Pij[27] <= 6.6
 -8.1 <= Pij[28] <= 8.1
 -8.1 <= Pij[29] <= 8.1
 -8.1 <= Pij[30] <= 8.1
 -8.1 <= Pij[31] <= 8.1
 -6.6 <= Pij[32] <= 6.6
 -7.2 <= Pij[33] <= 7.2
 -8.1 <= Pij[34] <= 8.1
 -6 <= Pij[35] <= 6
 -8.1 <= Pij[36] <= 8.1
 -8.1 <= Pij[37] <= 8.1
 -6 <= Pij[38] <= 6
 -8.1 <= Pij[39] <= 8.1
 -8.1 <= Pij[40] <= 8.1
 -6 <= Pij[41] <= 6
 -6 <= Pij[42] <= 6
 -8.1 <= Pij[43] <= 8.1
 -8.1 <= Pij[44] <= 8.1
 -42 <= Pij[45] <= 42
 -6 <= Pij[46] <= 6
 -54 <= Pij[47] <= 54
 -54 <= Pij[48] <= 54
 -54 <= Pij[49] <= 54
 -18 <= Pij[50] <= 18
 -8.1 <= Pij[51] <= 8.1
 -8.1 <= Pij[52] <= 8.1
 -60 <= Pij[53] <= 60
 -7.2 <= Pij[54] <= 7.2
 -8.1 <= Pij[55] <= 8.1
 -54 <= Pij[56] <= 54
 -54 <= Pij[57] <= 54
 -42 <= Pij[58] <= 42
 -51 <= Pij[59] <= 51
 -60 <= Pij[60] <= 60
 -42 <= Pij[61] <= 42
 -60 <= Pij[62] <= 60
 -60 <= Pij[63] <= 60
 -60 <= Pij[64] <= 60
 -8.1 <= Pij[65] <= 8.1
 -8.1 <= Pij[66] <= 8.1
 -39 <= Pij[67] <= 39
 -36 <= Pij[68] <= 36
 -45 <= Pij[69] <= 45
 -42 <= Pij[70] <= 42
 -60 <= Pij[71] <= 60
 -5.4 <= Pij[72] <= 5.4
 -18 <= Pij[73] <= 18
 -18 <= Pij[74] <= 18
 -18 <= Pij[75] <= 18
 -18 <= Pij[76] <= 18
 -18 <= Pij[77] <= 18
 -18 <= Pij[78] <= 18
 -2.7 <= Pa[0] <= 2.7
 -5.4 <= Pa[1] <= 5.4
 -2.7 <= Pa[2] <= 2.7
 -2.7 <= Pa[3] <= 2.7
 -2.7 <= Pa[4] <= 2.7
 -2.7 <= Pa[5] <= 2.7
 -5.4 <= Pa[6] <= 5.4
 -5.4 <= Pa[7] <= 5.4
 -2.4 <= Pa[8] <= 2.4
 -4.4 <= Pa[9] <= 4.4
 -5.4 <= Pa[10] <= 5.4
 -4.8 <= Pa[11] <= 4.8
 -2.2 <= Pa[12] <= 2.2
 -2.7 <= Pa[13] <= 2.7
 -2 <= Pa[14] <= 2
 -15 <= Pa[15] <= 15
 -20 <= Pa[16] <= 20
 -20 <= Pa[17] <= 20
 -2.2 <= Pa[18] <= 2.2
 -2.7 <= Pa[19] <= 2.7
 -2.7 <= Pa[20] <= 2.7
 -5.4 <= Pa[21] <= 5.4
 -5.4 <= Pa[22] <= 5.4
 -5.4 <= Pa[23] <= 5.4
 -2.2 <= Pa[24] <= 2.2
 -2.4 <= Pa[25] <= 2.4
 -2.7 <= Pa[26] <= 2.7
 -2.7 <= Pa[27] <= 2.7
 -4 <= Pa[28] <= 4
 -2.7 <= Pa[29] <= 2.7
 -5.4 <= Pa[30] <= 5.4
 -2 <= Pa[31] <= 2
 -2.7 <= Pa[32] <= 2.7
 -2.7 <= Pa[33] <= 2.7
 -2 <= Pa[34] <= 2
 -6 <= Pa[35] <= 6
 -2.7 <= Pa[36] <= 2.7
 -8.1 <= Pa[37] <= 8.1
 -14 <= Pa[38] <= 14
 -2.7 <= Pa[39] <= 2.7
 -2 <= Pa[40] <= 2
 -18 <= Pa[41] <= 18
 -18 <= Pa[42] <= 18
 -18 <= Pa[43] <= 18
 -6 <= Pa[44] <= 6
 -6 <= Pa[45] <= 6
 -6 <= Pa[46] <= 6
Generals
 n[0] n[1] n[2] n[3] n[4] n[5] n[6] n[7] n[8] n[9] n[10] n[11] n[12] n[13]
 n[14] n[15] n[16] n[17] n[18] n[19] n[20] n[21] n[22] n[23] n[24] n[25]
 n[26] n[27] n[28] n[29] n[30] n[31] n[32] n[33] n[34] n[35] n[36] n[37]
 n[38] n[39] n[40] n[41] n[42] n[43] n[44] n[45] n[46] n[47] n[48] n[49]
 n[50] n[51] n[52] n[53] n[54] n[55] n[56] n[57] n[58] n[59] n[60] n[61]
 n[62] n[63] n[64] n[65] n[66] n[67] n[68] n[69] n[70] n[71] n[72] n[73]
 n[74] n[75] n[76] n[77] n[78]
End

\ Model TNEP_MILP_bigM_Villasana
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x14b9a73051d6a32
Minimize
  200 w[0,1] + 400 w[0,2] + 600 w[0,3] + 800 w[0,4] + 1000 w[0,5]
   + 190 w[1,1] + 380 w[1,2] + 570 w[1,3] + 760 w[1,4] + 950 w[1,5]
   + 300 w[2,1] + 600 w[2,2] + 900 w[2,3] + 1200 w[2,4] + 1500 w[2,5]
   + 100 w[3,1] + 200 w[3,2] + 300 w[3,3] + 400 w[3,4] + 500 w[3,5]
   + 340 w[4,1] + 680 w[4,2] + 1020 w[4,3] + 1360 w[4,4] + 1700 w[4,5]
   + 100 w[5,1] + 200 w[5,2] + 300 w[5,3] + 400 w[5,4] + 500 w[5,5]
   + 200 w[6,1] + 400 w[6,2] + 600 w[6,3] + 800 w[6,4] + 1000 w[6,5]
   + 155 w[7,1] + 310 w[7,2] + 465 w[7,3] + 620 w[7,4] + 775 w[7,5]
   + 150 w[8,1] + 300 w[8,2] + 450 w[8,3] + 600 w[8,4] + 750 w[8,5]
   + 295 w[9,1] + 590 w[9,2] + 885 w[9,3] + 1180 w[9,4] + 1475 w[9,5]
   + 100 w[10,1] + 200 w[10,2] + 300 w[10,3] + 400 w[10,4] + 500 w[10,5]
   + 240 w[11,1] + 480 w[11,2] + 720 w[11,3] + 960 w[11,4] + 1200 w[11,5]
   + 315 w[12,1] + 630 w[12,2] + 945 w[12,3] + 1260 w[12,4] + 1575 w[12,5]
   + 150 w[13,1] + 300 w[13,2] + 450 w[13,3] + 600 w[13,4] + 750 w[13,5]
   + 305 w[14,1] + 610 w[14,2] + 915 w[14,3] + 1220 w[14,4] + 1525 w[14,5]
Subject To
 flujo_existente_1-2_0: - 2.5 theta[0] + 2.5 theta[1] + Pa[0] = 0
 flujo_existente_1-4_1: - 1.666666666666667 theta[0]
   + 1.666666666666667 theta[3] + Pa[1] = 0
 flujo_existente_1-5_2: - 5 theta[0] + 5 theta[4] + Pa[2] = 0
 flujo_existente_2-3_3: - 5 theta[1] + 5 theta[2] + Pa[3] = 0
 flujo_existente_2-4_4: - 2.5 theta[1] + 2.5 theta[3] + Pa[4] = 0
 flujo_existente_3-5_5: - 5 theta[2] + 5 theta[4] + Pa[5] = 0
 cap_sup_1-2_1: - w[0,1] + 2.5 dtheta[0,1] <= 0
 cap_inf_1-2_1: w[0,1] + 2.5 dtheta[0,1] >= 0
 cap_sup_1-2_2: - 2 w[0,2] + 5 dtheta[0,2] <= 0
 cap_inf_1-2_2: 2 w[0,2] + 5 dtheta[0,2] >= 0
 cap_sup_1-2_3: - 3 w[0,3] + 7.5 dtheta[0,3] <= 0
 cap_inf_1-2_3: 3 w[0,3] + 7.5 dtheta[0,3] >= 0
 cap_sup_1-2_4: - 4 w[0,4] + 10 dtheta[0,4] <= 0
 cap_inf_1-2_4: 4 w[0,4] + 10 dtheta[0,4] >= 0
 cap_sup_1-2_5: - 5 w[0,5] + 12.5 dtheta[0,5] <= 0
 cap_inf_1-2_5: 5 w[0,5] + 12.5 dtheta[0,5] >= 0
 bigM_sup_1-2: theta[0] - theta[1] + w[0,1] + w[0,2] + w[0,3] + w[0,4]
   + w[0,5] - dtheta[0,1] - dtheta[0,2] - dtheta[0,3] - dtheta[0,4]
   - dtheta[0,5] <= 1
 bigM_inf_1-2: theta[0] - theta[1] - w[0,1] - w[0,2] - w[0,3] - w[0,4]
   - w[0,5] - dtheta[0,1] - dtheta[0,2] - dtheta[0,3] - dtheta[0,4]
   - dtheta[0,5] >= -1
 unicidad_1-2: w[0,1] + w[0,2] + w[0,3] + w[0,4] + w[0,5] <= 1
 cap_sup_1-3_1: - w[1,1] + 2.631578947368421 dtheta[1,1] <= 0
 cap_inf_1-3_1: w[1,1] + 2.631578947368421 dtheta[1,1] >= 0
 cap_sup_1-3_2: - 2 w[1,2] + 5.263157894736842 dtheta[1,2] <= 0
 cap_inf_1-3_2: 2 w[1,2] + 5.263157894736842 dtheta[1,2] >= 0
 cap_sup_1-3_3: - 3 w[1,3] + 7.894736842105264 dtheta[1,3] <= 0
 cap_inf_1-3_3: 3 w[1,3] + 7.894736842105264 dtheta[1,3] >= 0
 cap_sup_1-3_4: - 4 w[1,4] + 10.52631578947368 dtheta[1,4] <= 0
 cap_inf_1-3_4: 4 w[1,4] + 10.52631578947368 dtheta[1,4] >= 0
 cap_sup_1-3_5: - 5 w[1,5] + 13.15789473684211 dtheta[1,5] <= 0
 cap_inf_1-3_5: 5 w[1,5] + 13.15789473684211 dtheta[1,5] >= 0
 bigM_sup_1-3: theta[0] - theta[2] + w[1,1] + w[1,2] + w[1,3] + w[1,4]
   + w[1,5] - dtheta[1,1] - dtheta[1,2] - dtheta[1,3] - dtheta[1,4]
   - dtheta[1,5] <= 1
 bigM_inf_1-3: theta[0] - theta[2] - w[1,1] - w[1,2] - w[1,3] - w[1,4]
   - w[1,5] - dtheta[1,1] - dtheta[1,2] - dtheta[1,3] - dtheta[1,4]
   - dtheta[1,5] >= -1
 unicidad_1-3: w[1,1] + w[1,2] + w[1,3] + w[1,4] + w[1,5] <= 1
 cap_sup_1-4_1: - 0.8 w[2,1] + 1.666666666666667 dtheta[2,1] <= 0
 cap_inf_1-4_1: 0.8 w[2,1] + 1.666666666666667 dtheta[2,1] >= 0
 cap_sup_1-4_2: - 1.6 w[2,2] + 3.333333333333333 dtheta[2,2] <= 0
 cap_inf_1-4_2: 1.6 w[2,2] + 3.333333333333333 dtheta[2,2] >= 0
 cap_sup_1-4_3: - 2.4 w[2,3] + 5 dtheta[2,3] <= 0
 cap_inf_1-4_3: 2.4 w[2,3] + 5 dtheta[2,3] >= 0
 cap_sup_1-4_4: - 3.2 w[2,4] + 6.666666666666667 dtheta[2,4] <= 0
 cap_inf_1-4_4: 3.2 w[2,4] + 6.666666666666667 dtheta[2,4] >= 0
 cap_sup_1-4_5: - 4 w[2,5] + 8.333333333333334 dtheta[2,5] <= 0
 cap_inf_1-4_5: 4 w[2,5] + 8.333333333333334 dtheta[2,5] >= 0
 bigM_sup_1-4: theta[0] - theta[3] + w[2,1] + w[2,2] + w[2,3] + w[2,4]
   + w[2,5] - dtheta[2,1] - dtheta[2,2] - dtheta[2,3] - dtheta[2,4]
   - dtheta[2,5] <= 1
 bigM_inf_1-4: theta[0] - theta[3] - w[2,1] - w[2,2] - w[2,3] - w[2,4]
   - w[2,5] - dtheta[2,1] - dtheta[2,2] - dtheta[2,3] - dtheta[2,4]
   - dtheta[2,5] >= -1
 unicidad_1-4: w[2,1] + w[2,2] + w[2,3] + w[2,4] + w[2,5] <= 1
 cap_sup_1-5_1: - w[3,1] + 5 dtheta[3,1] <= 0
 cap_inf_1-5_1: w[3,1] + 5 dtheta[3,1] >= 0
 cap_sup_1-5_2: - 2 w[3,2] + 10 dtheta[3,2] <= 0
 cap_inf_1-5_2: 2 w[3,2] + 10 dtheta[3,2] >= 0
 cap_sup_1-5_3: - 3 w[3,3] + 15 dtheta[3,3] <= 0
 cap_inf_1-5_3: 3 w[3,3] + 15 dtheta[3,3] >= 0
 cap_sup_1-5_4: - 4 w[3,4] + 20 dtheta[3,4] <= 0
 cap_inf_1-5_4: 4 w[3,4] + 20 dtheta[3,4] >= 0
 cap_sup_1-5_5: - 5 w[3,5] + 25 dtheta[3,5] <= 0
 cap_inf_1-5_5: 5 w[3,5] + 25 dtheta[3,5] >= 0
 bigM_sup_1-5: theta[0] - theta[4] + w[3,1] + w[3,2] + w[3,3] + w[3,4]
   + w[3,5] - dtheta[3,1] - dtheta[3,2] - dtheta[3,3] - dtheta[3,4]
   - dtheta[3,5] <= 1
 bigM_inf_1-5: theta[0] - theta[4] - w[3,1] - w[3,2] - w[3,3] - w[3,4]
   - w[3,5] - dtheta[3,1] - dtheta[3,2] - dtheta[3,3] - dtheta[3,4]
   - dtheta[3,5] >= -1
 unicidad_1-5: w[3,1] + w[3,2] + w[3,3] + w[3,4] + w[3,5] <= 1
 cap_sup_1-6_1: - 0.7 w[4,1] + 1.470588235294118 dtheta[4,1] <= 0
 cap_inf_1-6_1: 0.7 w[4,1] + 1.470588235294118 dtheta[4,1] >= 0
 cap_sup_1-6_2: - 1.4 w[4,2] + 2.941176470588235 dtheta[4,2] <= 0
 cap_inf_1-6_2: 1.4 w[4,2] + 2.941176470588235 dtheta[4,2] >= 0
 cap_sup_1-6_3: - 2.1 w[4,3] + 4.411764705882352 dtheta[4,3] <= 0
 cap_inf_1-6_3: 2.1 w[4,3] + 4.411764705882352 dtheta[4,3] >= 0
 cap_sup_1-6_4: - 2.8 w[4,4] + 5.88235294117647 dtheta[4,4] <= 0
 cap_inf_1-6_4: 2.8 w[4,4] + 5.88235294117647 dtheta[4,4] >= 0
 cap_sup_1-6_5: - 3.5 w[4,5] + 7.352941176470588 dtheta[4,5] <= 0
 cap_inf_1-6_5: 3.5 w[4,5] + 7.352941176470588 dtheta[4,5] >= 0
 bigM_sup_1-6: theta[0] - theta[5] + w[4,1] + w[4,2] + w[4,3] + w[4,4]
   + w[4,5] - dtheta[4,1] - dtheta[4,2] - dtheta[4,3] - dtheta[4,4]
   - dtheta[4,5] <= 1
 bigM_inf_1-6: theta[0] - theta[5] - w[4,1] - w[4,2] - w[4,3] - w[4,4]
   - w[4,5] - dtheta[4,1] - dtheta[4,2] - dtheta[4,3] - dtheta[4,4]
   - dtheta[4,5] >= -1
 unicidad_1-6: w[4,1] + w[4,2] + w[4,3] + w[4,4] + w[4,5] <= 1
 cap_sup_2-3_1: - w[5,1] + 5 dtheta[5,1] <= 0
 cap_inf_2-3_1: w[5,1] + 5 dtheta[5,1] >= 0
 cap_sup_2-3_2: - 2 w[5,2] + 10 dtheta[5,2] <= 0
 cap_inf_2-3_2: 2 w[5,2] + 10 dtheta[5,2] >= 0
 cap_sup_2-3_3: - 3 w[5,3] + 15 dtheta[5,3] <= 0
 cap_inf_2-3_3: 3 w[5,3] + 15 dtheta[5,3] >= 0
 cap_sup_2-3_4: - 4 w[5,4] + 20 dtheta[5,4] <= 0
 cap_inf_2-3_4: 4 w[5,4] + 20 dtheta[5,4] >= 0
 cap_sup_2-3_5: - 5 w[5,5] + 25 dtheta[5,5] <= 0
 cap_inf_2-3_5: 5 w[5,5] + 25 dtheta[5,5] >= 0
 bigM_sup_2-3: theta[1] - theta[2] + w[5,1] + w[5,2] + w[5,3] + w[5,4]
   + w[5,5] - dtheta[5,1] - dtheta[5,2] - dtheta[5,3] - dtheta[5,4]
   - dtheta[5,5] <= 1
 bigM_inf_2-3: theta[1] - theta[2] - w[5,1] - w[5,2] - w[5,3] - w[5,4]
   - w[5,5] - dtheta[5,1] - dtheta[5,2] - dtheta[5,3] - dtheta[5,4]
   - dtheta[5,5] >= -1
 unicidad_2-3: w[5,1] + w[5,2] + w[5,3] + w[5,4] + w[5,5] <= 1
 cap_sup_2-4_1: - w[6,1] + 2.5 dtheta[6,1] <= 0
 cap_inf_2-4_1: w[6,1] + 2.5 dtheta[6,1] >= 0
 cap_sup_2-4_2: - 2 w[6,2] + 5 dtheta[6,2] <= 0
 cap_inf_2-4_2: 2 w[6,2] + 5 dtheta[6,2] >= 0
 cap_sup_2-4_3: - 3 w[6,3] + 7.5 dtheta[6,3] <= 0
 cap_inf_2-4_3: 3 w[6,3] + 7.5 dtheta[6,3] >= 0
 cap_sup_2-4_4: - 4 w[6,4] + 10 dtheta[6,4] <= 0
 cap_inf_2-4_4: 4 w[6,4] + 10 dtheta[6,4] >= 0
 cap_sup_2-4_5: - 5 w[6,5] + 12.5 dtheta[6,5] <= 0
 cap_inf_2-4_5: 5 w[6,5] + 12.5 dtheta[6,5] >= 0
 bigM_sup_2-4: theta[1] - theta[3] + w[6,1] + w[6,2] + w[6,3] + w[6,4]
   + w[6,5] - dtheta[6,1] - dtheta[6,2] - dtheta[6,3] - dtheta[6,4]
   - dtheta[6,5] <= 1
 bigM_inf_2-4: theta[1] - theta[3] - w[6,1] - w[6,2] - w[6,3] - w[6,4]
   - w[6,5] - dtheta[6,1] - dtheta[6,2] - dtheta[6,3] - dtheta[6,4]
   - dtheta[6,5] >= -1
 unicidad_2-4: w[6,1] + w[6,2] + w[6,3] + w[6,4] + w[6,5] <= 1
 cap_sup_2-5_1: - w[7,1] + 3.225806451612903 dtheta[7,1] <= 0
 cap_inf_2-5_1: w[7,1] + 3.225806451612903 dtheta[7,1] >= 0
 cap_sup_2-5_2: - 2 w[7,2] + 6.451612903225807 dtheta[7,2] <= 0
 cap_inf_2-5_2: 2 w[7,2] + 6.451612903225807 dtheta[7,2] >= 0
 cap_sup_2-5_3: - 3 w[7,3] + 9.67741935483871 dtheta[7,3] <= 0
 cap_inf_2-5_3: 3 w[7,3] + 9.67741935483871 dtheta[7,3] >= 0
 cap_sup_2-5_4: - 4 w[7,4] + 12.90322580645161 dtheta[7,4] <= 0
 cap_inf_2-5_4: 4 w[7,4] + 12.90322580645161 dtheta[7,4] >= 0
 cap_sup_2-5_5: - 5 w[7,5] + 16.12903225806452 dtheta[7,5] <= 0
 cap_inf_2-5_5: 5 w[7,5] + 16.12903225806452 dtheta[7,5] >= 0
 bigM_sup_2-5: theta[1] - theta[4] + w[7,1] + w[7,2] + w[7,3] + w[7,4]
   + w[7,5] - dtheta[7,1] - dtheta[7,2] - dtheta[7,3] - dtheta[7,4]
   - dtheta[7,5] <= 1
 bigM_inf_2-5: theta[1] - theta[4] - w[7,1] - w[7,2] - w[7,3] - w[7,4]
   - w[7,5] - dtheta[7,1] - dtheta[7,2] - dtheta[7,3] - dtheta[7,4]
   - dtheta[7,5] >= -1
 unicidad_2-5: w[7,1] + w[7,2] + w[7,3] + w[7,4] + w[7,5] <= 1
 cap_sup_2-6_1: - w[8,1] + 3.333333333333333 dtheta[8,1] <= 0
 cap_inf_2-6_1: w[8,1] + 3.333333333333333 dtheta[8,1] >= 0
 cap_sup_2-6_2: - 2 w[8,2] + 6.666666666666667 dtheta[8,2] <= 0
 cap_inf_2-6_2: 2 w[8,2] + 6.666666666666667 dtheta[8,2] >= 0
 cap_sup_2-6_3: - 3 w[8,3] + 10 dtheta[8,3] <= 0
 cap_inf_2-6_3: 3 w[8,3] + 10 dtheta[8,3] >= 0
 cap_sup_2-6_4: - 4 w[8,4] + 13.33333333333333 dtheta[8,4] <= 0
 cap_inf_2-6_4: 4 w[8,4] + 13.33333333333333 dtheta[8,4] >= 0
 cap_sup_2-6_5: - 5 w[8,5] + 16.66666666666667 dtheta[8,5] <= 0
 cap_inf_2-6_5: 5 w[8,5] + 16.66666666666667 dtheta[8,5] >= 0
 bigM_sup_2-6: theta[1] - theta[5] + w[8,1] + w[8,2] + w[8,3] + w[8,4]
   + w[8,5] - dtheta[8,1] - dtheta[8,2] - dtheta[8,3] - dtheta[8,4]
   - dtheta[8,5] <= 1
 bigM_inf_2-6: theta[1] - theta[5] - w[8,1] - w[8,2] - w[8,3] - w[8,4]
   - w[8,5] - dtheta[8,1] - dtheta[8,2] - dtheta[8,3] - dtheta[8,4]
   - dtheta[8,5] >= -1
 unicidad_2-6: w[8,1] + w[8,2] + w[8,3] + w[8,4] + w[8,5] <= 1
 cap_sup_3-4_1: - 0.82 w[9,1] + 1.694915254237288 dtheta[9,1] <= 0
 cap_inf_3-4_1: 0.82 w[9,1] + 1.694915254237288 dtheta[9,1] >= 0
 cap_sup_3-4_2: - 1.64 w[9,2] + 3.389830508474577 dtheta[9,2] <= 0
 cap_inf_3-4_2: 1.64 w[9,2] + 3.389830508474577 dtheta[9,2] >= 0
 cap_sup_3-4_3: - 2.46 w[9,3] + 5.084745762711865 dtheta[9,3] <= 0
 cap_inf_3-4_3: 2.46 w[9,3] + 5.084745762711865 dtheta[9,3] >= 0
 cap_sup_3-4_4: - 3.28 w[9,4] + 6.779661016949153 dtheta[9,4] <= 0
 cap_inf_3-4_4: 3.28 w[9,4] + 6.779661016949153 dtheta[9,4] >= 0
 cap_sup_3-4_5: - 4.1 w[9,5] + 8.474576271186441 dtheta[9,5] <= 0
 cap_inf_3-4_5: 4.1 w[9,5] + 8.474576271186441 dtheta[9,5] >= 0
 bigM_sup_3-4: theta[2] - theta[3] + w[9,1] + w[9,2] + w[9,3] + w[9,4]
   + w[9,5] - dtheta[9,1] - dtheta[9,2] - dtheta[9,3] - dtheta[9,4]
   - dtheta[9,5] <= 1
 bigM_inf_3-4: theta[2] - theta[3] - w[9,1] - w[9,2] - w[9,3] - w[9,4]
   - w[9,5] - dtheta[9,1] - dtheta[9,2] - dtheta[9,3] - dtheta[9,4]
   - dtheta[9,5] >= -1
 unicidad_3-4: w[9,1] + w[9,2] + w[9,3] + w[9,4] + w[9,5] <= 1
 cap_sup_3-5_1: - w[10,1] + 5 dtheta[10,1] <= 0
 cap_inf_3-5_1: w[10,1] + 5 dtheta[10,1] >= 0
 cap_sup_3-5_2: - 2 w[10,2] + 10 dtheta[10,2] <= 0
 cap_inf_3-5_2: 2 w[10,2] + 10 dtheta[10,2] >= 0
 cap_sup_3-5_3: - 3 w[10,3] + 15 dtheta[10,3] <= 0
 cap_inf_3-5_3: 3 w[10,3] + 15 dtheta[10,3] >= 0
 cap_sup_3-5_4: - 4 w[10,4] + 20 dtheta[10,4] <= 0
 cap_inf_3-5_4: 4 w[10,4] + 20 dtheta[10,4] >= 0
 cap_sup_3-5_5: - 5 w[10,5] + 25 dtheta[10,5] <= 0
 cap_inf_3-5_5: 5 w[10,5] + 25 dtheta[10,5] >= 0
 bigM_sup_3-5: theta[2] - theta[4] + w[10,1] + w[10,2] + w[10,3] + w[10,4]
   + w[10,5] - dtheta[10,1] - dtheta[10,2] - dtheta[10,3] - dtheta[10,4]
   - dtheta[10,5] <= 1
 bigM_inf_3-5: theta[2] - theta[4] - w[10,1] - w[10,2] - w[10,3] - w[10,4]
   - w[10,5] - dtheta[10,1] - dtheta[10,2] - dtheta[10,3] - dtheta[10,4]
   - dtheta[10,5] >= -1
 unicidad_3-5: w[10,1] + w[10,2] + w[10,3] + w[10,4] + w[10,5] <= 1
 cap_sup_3-6_1: - w[11,1] + 2.083333333333333 dtheta[11,1] <= 0
 cap_inf_3-6_1: w[11,1] + 2.083333333333333 dtheta[11,1] >= 0
 cap_sup_3-6_2: - 2 w[11,2] + 4.166666666666667 dtheta[11,2] <= 0
 cap_inf_3-6_2: 2 w[11,2] + 4.166666666666667 dtheta[11,2] >= 0
 cap_sup_3-6_3: - 3 w[11,3] + 6.25 dtheta[11,3] <= 0
 cap_inf_3-6_3: 3 w[11,3] + 6.25 dtheta[11,3] >= 0
 cap_sup_3-6_4: - 4 w[11,4] + 8.333333333333334 dtheta[11,4] <= 0
 cap_inf_3-6_4: 4 w[11,4] + 8.333333333333334 dtheta[11,4] >= 0
 cap_sup_3-6_5: - 5 w[11,5] + 10.41666666666667 dtheta[11,5] <= 0
 cap_inf_3-6_5: 5 w[11,5] + 10.41666666666667 dtheta[11,5] >= 0
 bigM_sup_3-6: theta[2] - theta[5] + w[11,1] + w[11,2] + w[11,3] + w[11,4]
   + w[11,5] - dtheta[11,1] - dtheta[11,2] - dtheta[11,3] - dtheta[11,4]
   - dtheta[11,5] <= 1
 bigM_inf_3-6: theta[2] - theta[5] - w[11,1] - w[11,2] - w[11,3] - w[11,4]
   - w[11,5] - dtheta[11,1] - dtheta[11,2] - dtheta[11,3] - dtheta[11,4]
   - dtheta[11,5] >= -1
 unicidad_3-6: w[11,1] + w[11,2] + w[11,3] + w[11,4] + w[11,5] <= 1
 cap_sup_4-5_1: - 0.75 w[12,1] + 1.587301587301587 dtheta[12,1] <= 0
 cap_inf_4-5_1: 0.75 w[12,1] + 1.587301587301587 dtheta[12,1] >= 0
 cap_sup_4-5_2: - 1.5 w[12,2] + 3.174603174603174 dtheta[12,2] <= 0
 cap_inf_4-5_2: 1.5 w[12,2] + 3.174603174603174 dtheta[12,2] >= 0
 cap_sup_4-5_3: - 2.25 w[12,3] + 4.761904761904762 dtheta[12,3] <= 0
 cap_inf_4-5_3: 2.25 w[12,3] + 4.761904761904762 dtheta[12,3] >= 0
 cap_sup_4-5_4: - 3 w[12,4] + 6.349206349206349 dtheta[12,4] <= 0
 cap_inf_4-5_4: 3 w[12,4] + 6.349206349206349 dtheta[12,4] >= 0
 cap_sup_4-5_5: - 3.75 w[12,5] + 7.936507936507936 dtheta[12,5] <= 0
 cap_inf_4-5_5: 3.75 w[12,5] + 7.936507936507936 dtheta[12,5] >= 0
 bigM_sup_4-5: theta[3] - theta[4] + w[12,1] + w[12,2] + w[12,3] + w[12,4]
   + w[12,5] - dtheta[12,1] - dtheta[12,2] - dtheta[12,3] - dtheta[12,4]
   - dtheta[12,5] <= 1
 bigM_inf_4-5: theta[3] - theta[4] - w[12,1] - w[12,2] - w[12,3] - w[12,4]
   - w[12,5] - dtheta[12,1] - dtheta[12,2] - dtheta[12,3] - dtheta[12,4]
   - dtheta[12,5] >= -1
 unicidad_4-5: w[12,1] + w[12,2] + w[12,3] + w[12,4] + w[12,5] <= 1
 cap_sup_4-6_1: - w[13,1] + 3.333333333333333 dtheta[13,1] <= 0
 cap_inf_4-6_1: w[13,1] + 3.333333333333333 dtheta[13,1] >= 0
 cap_sup_4-6_2: - 2 w[13,2] + 6.666666666666667 dtheta[13,2] <= 0
 cap_inf_4-6_2: 2 w[13,2] + 6.666666666666667 dtheta[13,2] >= 0
 cap_sup_4-6_3: - 3 w[13,3] + 10 dtheta[13,3] <= 0
 cap_inf_4-6_3: 3 w[13,3] + 10 dtheta[13,3] >= 0
 cap_sup_4-6_4: - 4 w[13,4] + 13.33333333333333 dtheta[13,4] <= 0
 cap_inf_4-6_4: 4 w[13,4] + 13.33333333333333 dtheta[13,4] >= 0
 cap_sup_4-6_5: - 5 w[13,5] + 16.66666666666667 dtheta[13,5] <= 0
 cap_inf_4-6_5: 5 w[13,5] + 16.66666666666667 dtheta[13,5] >= 0
 bigM_sup_4-6: theta[3] - theta[5] + w[13,1] + w[13,2] + w[13,3] + w[13,4]
   + w[13,5] - dtheta[13,1] - dtheta[13,2] - dtheta[13,3] - dtheta[13,4]
   - dtheta[13,5] <= 1
 bigM_inf_4-6: theta[3] - theta[5] - w[13,1] - w[13,2] - w[13,3] - w[13,4]
   - w[13,5] - dtheta[13,1] - dtheta[13,2] - dtheta[13,3] - dtheta[13,4]
   - dtheta[13,5] >= -1
 unicidad_4-6: w[13,1] + w[13,2] + w[13,3] + w[13,4] + w[13,5] <= 1
 cap_sup_5-6_1: - 0.78 w[14,1] + 1.639344262295082 dtheta[14,1] <= 0
 cap_inf_5-6_1: 0.78 w[14,1] + 1.639344262295082 dtheta[14,1] >= 0
 cap_sup_5-6_2: - 1.56 w[14,2] + 3.278688524590164 dtheta[14,2] <= 0
 cap_inf_5-6_2: 1.56 w[14,2] + 3.278688524590164 dtheta[14,2] >= 0
 cap_sup_5-6_3: - 2.34 w[14,3] + 4.918032786885246 dtheta[14,3] <= 0
 cap_inf_5-6_3: 2.34 w[14,3] + 4.918032786885246 dtheta[14,3] >= 0
 cap_sup_5-6_4: - 3.12 w[14,4] + 6.557377049180328 dtheta[14,4] <= 0
 cap_inf_5-6_4: 3.12 w[14,4] + 6.557377049180328 dtheta[14,4] >= 0
 cap_sup_5-6_5: - 3.9 w[14,5] + 8.196721311475411 dtheta[14,5] <= 0
 cap_inf_5-6_5: 3.9 w[14,5] + 8.196721311475411 dtheta[14,5] >= 0
 bigM_sup_5-6: theta[4] - theta[5] + w[14,1] + w[14,2] + w[14,3] + w[14,4]
   + w[14,5] - dtheta[14,1] - dtheta[14,2] - dtheta[14,3] - dtheta[14,4]
   - dtheta[14,5] <= 1
 bigM_inf_5-6: theta[4] - theta[5] - w[14,1] - w[14,2] - w[14,3] - w[14,4]
   - w[14,5] - dtheta[14,1] - dtheta[14,2] - dtheta[14,3] - dtheta[14,4]
   - dtheta[14,5] >= -1
 unicidad_5-6: w[14,1] + w[14,2] + w[14,3] + w[14,4] + w[14,5] <= 1
 balance_1: 2.5 dtheta[0,1] + 5 dtheta[0,2] + 7.5 dtheta[0,3]
   + 10 dtheta[0,4] + 12.5 dtheta[0,5] + 2.631578947368421 dtheta[1,1]
   + 5.263157894736842 dtheta[1,2] + 7.894736842105264 dtheta[1,3]
   + 10.52631578947368 dtheta[1,4] + 13.15789473684211 dtheta[1,5]
   + 1.666666666666667 dtheta[2,1] + 3.333333333333333 dtheta[2,2]
   + 5 dtheta[2,3] + 6.666666666666667 dtheta[2,4]
   + 8.333333333333334 dtheta[2,5] + 5 dtheta[3,1] + 10 dtheta[3,2]
   + 15 dtheta[3,3] + 20 dtheta[3,4] + 25 dtheta[3,5]
   + 1.470588235294118 dtheta[4,1] + 2.941176470588235 dtheta[4,2]
   + 4.411764705882352 dtheta[4,3] + 5.88235294117647 dtheta[4,4]
   + 7.352941176470588 dtheta[4,5] + Pa[0] + Pa[1] + Pa[2] = -0.3
 balance_2: - 2.5 dtheta[0,1] - 5 dtheta[0,2] - 7.5 dtheta[0,3]
   - 10 dtheta[0,4] - 12.5 dtheta[0,5] + 5 dtheta[5,1] + 10 dtheta[5,2]
   + 15 dtheta[5,3] + 20 dtheta[5,4] + 25 dtheta[5,5] + 2.5 dtheta[6,1]
   + 5 dtheta[6,2] + 7.5 dtheta[6,3] + 10 dtheta[6,4] + 12.5 dtheta[6,5]
   + 3.225806451612903 dtheta[7,1] + 6.451612903225807 dtheta[7,2]
   + 9.67741935483871 dtheta[7,3] + 12.90322580645161 dtheta[7,4]
   + 16.12903225806452 dtheta[7,5] + 3.333333333333333 dtheta[8,1]
   + 6.666666666666667 dtheta[8,2] + 10 dtheta[8,3]
   + 13.33333333333333 dtheta[8,4] + 16.66666666666667 dtheta[8,5] - Pa[0]
   + Pa[3] + Pa[4] = -2.4
 balance_3: - 2.631578947368421 dtheta[1,1] - 5.263157894736842 dtheta[1,2]
   - 7.894736842105264 dtheta[1,3] - 10.52631578947368 dtheta[1,4]
   - 13.15789473684211 dtheta[1,5] - 5 dtheta[5,1] - 10 dtheta[5,2]
   - 15 dtheta[5,3] - 20 dtheta[5,4] - 25 dtheta[5,5]
   + 1.694915254237288 dtheta[9,1] + 3.389830508474577 dtheta[9,2]
   + 5.084745762711865 dtheta[9,3] + 6.779661016949153 dtheta[9,4]
   + 8.474576271186441 dtheta[9,5] + 5 dtheta[10,1] + 10 dtheta[10,2]
   + 15 dtheta[10,3] + 20 dtheta[10,4] + 25 dtheta[10,5]
   + 2.083333333333333 dtheta[11,1] + 4.166666666666667 dtheta[11,2]
   + 6.25 dtheta[11,3] + 8.333333333333334 dtheta[11,4]
   + 10.41666666666667 dtheta[11,5] - Pa[3] + Pa[5] = 1.25
 balance_4: - 1.666666666666667 dtheta[2,1] - 3.333333333333333 dtheta[2,2]
   - 5 dtheta[2,3] - 6.666666666666667 dtheta[2,4]
   - 8.333333333333334 dtheta[2,5] - 2.5 dtheta[6,1] - 5 dtheta[6,2]
   - 7.5 dtheta[6,3] - 10 dtheta[6,4] - 12.5 dtheta[6,5]
   - 1.694915254237288 dtheta[9,1] - 3.389830508474577 dtheta[9,2]
   - 5.084745762711865 dtheta[9,3] - 6.779661016949153 dtheta[9,4]
   - 8.474576271186441 dtheta[9,5] + 1.587301587301587 dtheta[12,1]
   + 3.174603174603174 dtheta[12,2] + 4.761904761904762 dtheta[12,3]
   + 6.349206349206349 dtheta[12,4] + 7.936507936507936 dtheta[12,5]
   + 3.333333333333333 dtheta[13,1] + 6.666666666666667 dtheta[13,2]
   + 10 dtheta[13,3] + 13.33333333333333 dtheta[13,4]
   + 16.66666666666667 dtheta[13,5] - Pa[1] - Pa[4] = -1.6
 balance_5: - 5 dtheta[3,1] - 10 dtheta[3,2] - 15 dtheta[3,3]
   - 20 dtheta[3,4] - 25 dtheta[3,5] - 3.225806451612903 dtheta[7,1]
   - 6.451612903225807 dtheta[7,2] - 9.67741935483871 dtheta[7,3]
   - 12.90322580645161 dtheta[7,4] - 16.12903225806452 dtheta[7,5]
   - 5 dtheta[10,1] - 10 dtheta[10,2] - 15 dtheta[10,3] - 20 dtheta[10,4]
   - 25 dtheta[10,5] - 1.587301587301587 dtheta[12,1]
   - 3.174603174603174 dtheta[12,2] - 4.761904761904762 dtheta[12,3]
   - 6.349206349206349 dtheta[12,4] - 7.936507936507936 dtheta[12,5]
   + 1.639344262295082 dtheta[14,1] + 3.278688524590164 dtheta[14,2]
   + 4.918032786885246 dtheta[14,3] + 6.557377049180328 dtheta[14,4]
   + 8.196721311475411 dtheta[14,5] - Pa[2] - Pa[5] = -2.4
 balance_6: - 1.470588235294118 dtheta[4,1] - 2.941176470588235 dtheta[4,2]
   - 4.411764705882352 dtheta[4,3] - 5.88235294117647 dtheta[4,4]
   - 7.352941176470588 dtheta[4,5] - 3.333333333333333 dtheta[8,1]
   - 6.666666666666667 dtheta[8,2] - 10 dtheta[8,3]
   - 13.33333333333333 dtheta[8,4] - 16.66666666666667 dtheta[8,5]
   - 2.083333333333333 dtheta[11,1] - 4.166666666666667 dtheta[11,2]
   - 6.25 dtheta[11,3] - 8.333333333333334 dtheta[11,4]
   - 10.41666666666667 dtheta[11,5] - 3.333333333333333 dtheta[13,1]
   - 6.666666666666667 dtheta[13,2] - 10 dtheta[13,3]
   - 13.33333333333333 dtheta[13,4] - 16.66666666666667 dtheta[13,5]
   - 1.639344262295082 dtheta[14,1] - 3.278688524590164 dtheta[14,2]
   - 4.918032786885246 dtheta[14,3] - 6.557377049180328 dtheta[14,4]
   - 8.196721311475411 dtheta[14,5] = 5.45
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
 dtheta[0,5] free
 dtheta[1,1] free
 dtheta[1,2] free
 dtheta[1,3] free
 dtheta[1,4] free
 dtheta[1,5] free
 dtheta[2,1] free
 dtheta[2,2] free
 dtheta[2,3] free
 dtheta[2,4] free
 dtheta[2,5] free
 dtheta[3,1] free
 dtheta[3,2] free
 dtheta[3,3] free
 dtheta[3,4] free
 dtheta[3,5] free
 dtheta[4,1] free
 dtheta[4,2] free
 dtheta[4,3] free
 dtheta[4,4] free
 dtheta[4,5] free
 dtheta[5,1] free
 dtheta[5,2] free
 dtheta[5,3] free
 dtheta[5,4] free
 dtheta[5,5] free
 dtheta[6,1] free
 dtheta[6,2] free
 dtheta[6,3] free
 dtheta[6,4] free
 dtheta[6,5] free
 dtheta[7,1] free
 dtheta[7,2] free
 dtheta[7,3] free
 dtheta[7,4] free
 dtheta[7,5] free
 dtheta[8,1] free
 dtheta[8,2] free
 dtheta[8,3] free
 dtheta[8,4] free
 dtheta[8,5] free
 dtheta[9,1] free
 dtheta[9,2] free
 dtheta[9,3] free
 dtheta[9,4] free
 dtheta[9,5] free
 dtheta[10,1] free
 dtheta[10,2] free
 dtheta[10,3] free
 dtheta[10,4] free
 dtheta[10,5] free
 dtheta[11,1] free
 dtheta[11,2] free
 dtheta[11,3] free
 dtheta[11,4] free
 dtheta[11,5] free
 dtheta[12,1] free
 dtheta[12,2] free
 dtheta[12,3] free
 dtheta[12,4] free
 dtheta[12,5] free
 dtheta[13,1] free
 dtheta[13,2] free
 dtheta[13,3] free
 dtheta[13,4] free
 dtheta[13,5] free
 dtheta[14,1] free
 dtheta[14,2] free
 dtheta[14,3] free
 dtheta[14,4] free
 dtheta[14,5] free
 -1 <= Pa[0] <= 1
 -0.8 <= Pa[1] <= 0.8
 -1 <= Pa[2] <= 1
 -1 <= Pa[3] <= 1
 -1 <= Pa[4] <= 1
 -1 <= Pa[5] <= 1
Binaries
 w[0,1] w[0,2] w[0,3] w[0,4] w[0,5] w[1,1] w[1,2] w[1,3] w[1,4] w[1,5]
 w[2,1] w[2,2] w[2,3] w[2,4] w[2,5] w[3,1] w[3,2] w[3,3] w[3,4] w[3,5]
 w[4,1] w[4,2] w[4,3] w[4,4] w[4,5] w[5,1] w[5,2] w[5,3] w[5,4] w[5,5]
 w[6,1] w[6,2] w[6,3] w[6,4] w[6,5] w[7,1] w[7,2] w[7,3] w[7,4] w[7,5]
 w[8,1] w[8,2] w[8,3] w[8,4] w[8,5] w[9,1] w[9,2] w[9,3] w[9,4] w[9,5]
 w[10,1] w[10,2] w[10,3] w[10,4] w[10,5] w[11,1] w[11,2] w[11,3] w[11,4]
 w[11,5] w[12,1] w[12,2] w[12,3] w[12,4] w[12,5] w[13,1] w[13,2] w[13,3]
 w[13,4] w[13,5] w[14,1] w[14,2] w[14,3] w[14,4] w[14,5]
End

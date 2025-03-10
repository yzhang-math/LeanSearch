--@funsearch.evolve
theorem mathd_numbertheory_301 (j : ℕ) (h₀ : 0 < j) : 3 * (7 * ↑j + 3) % 7 = 2 := by
  calc
    3 * (7 * ↑j + 3) % 7 = (3 * 3 + 3 * ↑j * 7) % 7 := by ring_nf
    _ = 3 * 3 % 7 := by apply Nat.add_mul_mod_self_right
    _ = 2 := by norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

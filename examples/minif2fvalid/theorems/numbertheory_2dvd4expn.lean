--@funsearch.evolve
theorem numbertheory_2dvd4expn (n : ℕ) (h₀ : n ≠ 0) : 2 ∣ 4 ^ n := by
  revert n h₀
  rintro ⟨k, rfl⟩
  · norm_num
  apply dvd_pow
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

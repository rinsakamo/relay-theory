namespace RelayTheory
namespace LossyWorkload

abbrev History := Bool × Bool
abbrev Representation := Bool

def firstBit (h : History) : Bool := h.1
def secondBit (h : History) : Bool := h.2

def mismatch (prediction target : Bool) : Nat :=
  if prediction = target then 0 else 1

def totalError
    (encode : History → Representation)
    (query : History → Bool) : Nat :=
  mismatch (encode (false, false)) (query (false, false)) +
  mismatch (encode (false, true))  (query (false, true)) +
  mismatch (encode (true, false))  (query (true, false)) +
  mismatch (encode (true, true))   (query (true, true))

def firstBitErrors : Nat × Nat :=
  (totalError firstBit firstBit, totalError firstBit secondBit)

def secondBitErrors : Nat × Nat :=
  (totalError secondBit firstBit, totalError secondBit secondBit)

def weightedLoss (weights errors : Nat × Nat) : Nat :=
  weights.1 * errors.1 + weights.2 * errors.2

def firstHeavy : Nat × Nat := (2, 1)
def secondHeavy : Nat × Nat := (1, 2)

theorem firstBitErrors_exact :
    firstBitErrors = (0, 2) := by
  decide

theorem secondBitErrors_exact :
    secondBitErrors = (2, 0) := by
  decide

theorem firstHeavy_prefers_firstBit :
    weightedLoss firstHeavy firstBitErrors <
      weightedLoss firstHeavy secondBitErrors := by
  decide

theorem secondHeavy_prefers_secondBit :
    weightedLoss secondHeavy secondBitErrors <
      weightedLoss secondHeavy firstBitErrors := by
  decide

/--
The same history space and the same one-bit representation budget admit
opposite strict representation rankings when only the declared positive
future-query weights are swapped.
-/
theorem ranking_reverses_under_weight_swap :
    (weightedLoss firstHeavy firstBitErrors <
      weightedLoss firstHeavy secondBitErrors) ∧
    (weightedLoss secondHeavy secondBitErrors <
      weightedLoss secondHeavy firstBitErrors) := by
  exact ⟨firstHeavy_prefers_firstBit, secondHeavy_prefers_secondBit⟩

end LossyWorkload
end RelayTheory

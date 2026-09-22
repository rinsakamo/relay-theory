import RelayTheory.HabitSelectionTendencyCountermodel

namespace RelayTheory

namespace EmotionAppraisalModulationCountermodel

abbrev Bit := Bool
abbrev Appraisal := HabitSelectionTendencyCountermodel.Context
abbrev Response := HabitSelectionTendencyCountermodel.Response
abbrev SelectionWeight := HabitSelectionTendencyCountermodel.SelectionWeight

/--
Operational appraisal modulation: changing the declared appraisal coordinate
changes at least one response's selection weight.
-/
def AppraisalModulates (weights : SelectionWeight) : Prop :=
  ∃ r : Response, weights false r ≠ weights true r

/-- Neither Habit-like false dominance nor appraisal modulation. -/
def neitherProfile : SelectionWeight :=
  fun _ _ => 1

/-- Appraisal modulation without global false-dominant tendency. -/
def modulationOnlyProfile : SelectionWeight :=
  fun appraisal response =>
    if appraisal
    then if response then 1 else 2
    else 1

/-- Global false-dominant tendency without appraisal modulation. -/
def tendencyOnlyProfile : SelectionWeight :=
  fun _ response =>
    if response then 1 else 2

/-- Both global false-dominant tendency and appraisal modulation. -/
def bothProfile : SelectionWeight :=
  fun appraisal response =>
    if appraisal
    then if response then 1 else 3
    else if response then 1 else 2

theorem neither_not_falseDominant :
    ¬ HabitSelectionTendencyCountermodel.FalseDominant neitherProfile := by
  intro h
  have bad := h false
  simp [neitherProfile] at bad

theorem neither_not_appraisalModulates :
    ¬ AppraisalModulates neitherProfile := by
  intro h
  rcases h with ⟨r, hr⟩
  simp [neitherProfile] at hr

theorem modulationOnly_not_falseDominant :
    ¬ HabitSelectionTendencyCountermodel.FalseDominant modulationOnlyProfile := by
  intro h
  have bad := h false
  simp [modulationOnlyProfile] at bad

theorem modulationOnly_appraisalModulates :
    AppraisalModulates modulationOnlyProfile := by
  refine ⟨false, ?_⟩
  simp [modulationOnlyProfile]

theorem tendencyOnly_falseDominant :
    HabitSelectionTendencyCountermodel.FalseDominant tendencyOnlyProfile := by
  intro c
  simp [tendencyOnlyProfile]

theorem tendencyOnly_not_appraisalModulates :
    ¬ AppraisalModulates tendencyOnlyProfile := by
  intro h
  rcases h with ⟨r, hr⟩
  simp [tendencyOnlyProfile] at hr

theorem both_falseDominant :
    HabitSelectionTendencyCountermodel.FalseDominant bothProfile := by
  intro c
  cases c <;> simp [bothProfile]

theorem both_appraisalModulates :
    AppraisalModulates bothProfile := by
  refine ⟨false, ?_⟩
  simp [bothProfile]

/--
The non-habit pair has exactly the same baseline appraisal profile.
-/
theorem sameBaseline_neither_modulationOnly :
    ∀ r : Response, neitherProfile false r = modulationOnlyProfile false r := by
  intro r
  simp [neitherProfile, modulationOnlyProfile]

/--
The habit-like pair also has exactly the same baseline appraisal profile.
-/
theorem sameBaseline_tendencyOnly_both :
    ∀ r : Response, tendencyOnlyProfile false r = bothProfile false r := by
  intro r
  simp [tendencyOnlyProfile, bothProfile]

theorem neither_capable :
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      neitherProfile := by
  intro c
  refine ⟨c, ?_, rfl⟩
  simp [neitherProfile]

theorem modulationOnly_capable :
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      modulationOnlyProfile := by
  intro c
  refine ⟨c, ?_, rfl⟩
  cases c <;> simp [modulationOnlyProfile]

theorem tendencyOnly_capable :
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      tendencyOnlyProfile := by
  intro c
  refine ⟨c, ?_, rfl⟩
  cases c <;> simp [tendencyOnlyProfile]

theorem both_capable :
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      bothProfile := by
  intro c
  refine ⟨c, ?_, rfl⟩
  cases c <;> simp [bothProfile]

theorem allFour_tendencyModulationQuadrants :
    (¬ HabitSelectionTendencyCountermodel.FalseDominant neitherProfile ∧
      ¬ AppraisalModulates neitherProfile) ∧
    (¬ HabitSelectionTendencyCountermodel.FalseDominant modulationOnlyProfile ∧
      AppraisalModulates modulationOnlyProfile) ∧
    (HabitSelectionTendencyCountermodel.FalseDominant tendencyOnlyProfile ∧
      ¬ AppraisalModulates tendencyOnlyProfile) ∧
    (HabitSelectionTendencyCountermodel.FalseDominant bothProfile ∧
      AppraisalModulates bothProfile) := by
  exact ⟨
    ⟨neither_not_falseDominant, neither_not_appraisalModulates⟩,
    ⟨modulationOnly_not_falseDominant, modulationOnly_appraisalModulates⟩,
    ⟨tendencyOnly_falseDominant, tendencyOnly_not_appraisalModulates⟩,
    ⟨both_falseDominant, both_appraisalModulates⟩
  ⟩

theorem habitTendency_doesNotDetermineAppraisalModulation :
    HabitSelectionTendencyCountermodel.FalseDominant tendencyOnlyProfile ∧
    HabitSelectionTendencyCountermodel.FalseDominant bothProfile ∧
    ¬ AppraisalModulates tendencyOnlyProfile ∧
    AppraisalModulates bothProfile := by
  exact ⟨
    tendencyOnly_falseDominant,
    both_falseDominant,
    tendencyOnly_not_appraisalModulates,
    both_appraisalModulates
  ⟩

theorem appraisalModulation_doesNotDetermineHabitTendency :
    AppraisalModulates modulationOnlyProfile ∧
    AppraisalModulates bothProfile ∧
    ¬ HabitSelectionTendencyCountermodel.FalseDominant modulationOnlyProfile ∧
    HabitSelectionTendencyCountermodel.FalseDominant bothProfile := by
  exact ⟨
    modulationOnly_appraisalModulates,
    both_appraisalModulates,
    modulationOnly_not_falseDominant,
    both_falseDominant
  ⟩

theorem competence_doesNotDetermineAppraisalModulation :
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      neitherProfile ∧
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      modulationOnlyProfile ∧
    ¬ AppraisalModulates neitherProfile ∧
    AppraisalModulates modulationOnlyProfile := by
  exact ⟨
    neither_capable,
    modulationOnly_capable,
    neither_not_appraisalModulates,
    modulationOnly_appraisalModulates
  ⟩

theorem extensionalWeightsPreserveAppraisalModulation
    (f g : SelectionWeight)
    (hEq : ∀ a : Appraisal, ∀ r : Response, f a r = g a r) :
    AppraisalModulates f ↔ AppraisalModulates g := by
  constructor
  · intro hf
    rcases hf with ⟨r, hr⟩
    refine ⟨r, ?_⟩
    simpa [hEq false r, hEq true r] using hr
  · intro hg
    rcases hg with ⟨r, hr⟩
    refine ⟨r, ?_⟩
    simpa [← hEq false r, ← hEq true r] using hr

structure DecoratedWeights where
  base : SelectionWeight
  emotionFlag : Bit

def decoratedEmotionTrue : DecoratedWeights where
  base := bothProfile
  emotionFlag := true

def decoratedEmotionFalse : DecoratedWeights where
  base := bothProfile
  emotionFlag := false

theorem emotionLabelDeletion_modulation :
    AppraisalModulates decoratedEmotionTrue.base ↔
    AppraisalModulates decoratedEmotionFalse.base := by
  rfl

theorem emotionLabelDeletion_habitTendency :
    HabitSelectionTendencyCountermodel.FalseDominant decoratedEmotionTrue.base ↔
    HabitSelectionTendencyCountermodel.FalseDominant decoratedEmotionFalse.base := by
  rfl

/--
Combined scoped result:
- Habit-like default tendency and appraisal modulation realize all four Boolean
  combinations on one shared lower-level selection surface;
- matched pairs can share the entire baseline appraisal profile while differing
  under the alternate appraisal;
- all four profiles remain task-capable under the same #95 criterion;
- appraisal modulation is extensional in the full declared surface;
- a decorative Emotion label adds no information.
-/
theorem emotionHabitSeparation_bundle :
    (∀ r : Response,
      neitherProfile false r = modulationOnlyProfile false r) ∧
    (∀ r : Response,
      tendencyOnlyProfile false r = bothProfile false r) ∧
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      neitherProfile ∧
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      modulationOnlyProfile ∧
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      tendencyOnlyProfile ∧
    HabitSelectionTendencyCountermodel.Capable
      HabitSelectionTendencyCountermodel.identitySuccess
      bothProfile ∧
    ¬ HabitSelectionTendencyCountermodel.FalseDominant modulationOnlyProfile ∧
    AppraisalModulates modulationOnlyProfile ∧
    HabitSelectionTendencyCountermodel.FalseDominant tendencyOnlyProfile ∧
    ¬ AppraisalModulates tendencyOnlyProfile := by
  exact ⟨
    sameBaseline_neither_modulationOnly,
    sameBaseline_tendencyOnly_both,
    neither_capable,
    modulationOnly_capable,
    tendencyOnly_capable,
    both_capable,
    modulationOnly_not_falseDominant,
    modulationOnly_appraisalModulates,
    tendencyOnly_falseDominant,
    tendencyOnly_not_appraisalModulates
  ⟩

end EmotionAppraisalModulationCountermodel

end RelayTheory

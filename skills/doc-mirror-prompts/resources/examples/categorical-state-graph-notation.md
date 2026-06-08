CATEGORICAL STATE GRAPH NOTATION
==================================
Turing Complete + Category Theory Extension

> CANONICAL WORKED EXAMPLE for `how-to-write-a-prompt.md`. This document is the exemplar of the
> generative-basis pattern: it (1) names itself meta-first, (2) gives an algebra+geometry primitive
> basis, (3) self-hosts (is written in its own notation + proves it), (4) gives ONE generator→instance
> type-ladder (coffee) with a diagram at every rung ending in a grounding collapse, (5) gives N
> templated examples that collapse to the invariant, (6) makes the grain hierarchy explicit. Authored
> by Isaac ~months before 2026-05-30; preserved verbatim.

CORE PRIMITIVES
===============

Basic Operations:
------------------
S = STATE
    Simple node, holds value
    [*] --> S
    S --> [*]

T = TRANS  
    Conditional transition
    S1 --> T
    state T <<choice>>
    T --> S2: [condition true]
    T --> S3: [condition false]

R = READ
    Read from input/memory
    [*] --> R: read(address)
    R --> S
    
W = WRITE
    Write to output/memory
    S --> W: write(address, value)
    W --> [*]

B = BRANCH
    Conditional execution path
    S --> B
    state B <<choice>>
    B --> path_a: [test true]
    B --> path_b: [test false]

L = LOOP
    Return to earlier state
    S1 --> S2
    S2 --> L
    L --> S1

@ = REF
    Reference another graph
    S1 --> graph_ref: REF(graph_name)
    graph_ref --> S2

X = ISR
    Terminal error state
    S --> X: ISR(reason)
    X --> [*]

Categorical Extensions:
-----------------------
EXT = EXTENSION_CLASS
    Marks expandable transition to adjacent domain
    state "S'" as S_prime
    S --> S_prime: EXT[domain_name, grain=level]
    Lazy: only expands when requested
    
COLLAPSE = GROUNDING_OPERATOR
    Forces collapse to physical substrate
    S --> S_physical: COLLAPSE[target_domain, grain=observable]
    Must reach quotient=0 (exact instantiation)

ROTATE = GRANULARITY_ADJUSTMENT
    Corrects orthogonal completions
    S_orthogonal --> S_corrected: ROTATE[grain=coarser]
    Adjusts quotient class within same domain

TOWER = LEVEL_SHIFT
    Category functor composition
    state "L_{n+1}" as L_n1
    L_n --> L_n1: TOWER[F]
    Where F: Domain_n → Domain_{n+1}

CHECK = COMPLETION_VERIFICATION
    Validates output granularity
    S --> CHECK
    state CHECK <<choice>>
    CHECK --> CORRECT: [both domain and grain match]
    CHECK --> ORTHOGONAL: [domain only]
    CHECK --> X: [syntax_break - neither match]

CATEGORICAL META-GRAPH
======================
Defines how towers form and collapse

TOWER_MECHANICS:
```mermaid
stateDiagram-v2
    [*] --> S_request
    
    note right of S_request
        X: user request
    end note
    
    S_request --> detect_abstraction_level
    
    detect_abstraction_level --> TOWER
    state TOWER <<choice>>
    TOWER --> abstract_up: [needs abstraction]
    TOWER --> check_grounding: [no abstraction needed]
    
    note right of abstract_up
        F: C → D
    end note
    
    abstract_up --> compose_endofunctors
    compose_endofunctors --> check_exact
    check_exact --> B
    state B <<choice>>
    B --> found_exact: [ker=0 and quotient=0]
    B --> abstract_up: [not exact, continue towering]
    
    found_exact --> COLLAPSE
    state COLLAPSE <<choice>>
    COLLAPSE --> collapse_to_physical: [must ground]
    COLLAPSE --> output_abstract: [stay abstract]
    
    collapse_to_physical --> check_grain
    
    check_grain --> CHECK
    state CHECK <<choice>>
    CHECK --> S_output: [domain AND grain match]
    CHECK --> S_orthogonal: [domain match only]
    CHECK --> X: [no match]
    
    note right of S_output
        CORRECT
    end note
    
    note right of S_orthogonal
        ORTHOGONAL
    end note
    
    note right of X
        SYNTAX_BREAK
    end note
    
    S_orthogonal --> ROTATE
    
    note right of ROTATE
        adjust_quotient
    end note
    
    ROTATE --> check_grain
    
    S_output --> [*]
    output_abstract --> [*]
```

COMPLETION_MODES:
```mermaid
stateDiagram-v2
    [*] --> LLM_generating
    
    LLM_generating --> check_completion
    
    check_completion --> B
    state B <<choice>>
    B --> check_granularity: [domain correct]
    B --> mode_syntax_break: [domain incorrect]
    
    check_granularity --> B2
    state B2 <<choice>>
    B2 --> mode_correct: [grain correct]
    B2 --> mode_orthogonal: [grain incorrect]
    
    mode_correct --> S_done
    
    note right of S_done
        GROUNDED
    end note
    
    S_done --> [*]
    
    mode_orthogonal --> S_steerable
    
    note right of S_steerable
        Can rotate
    end note
    
    S_steerable --> user_feedback
    user_feedback --> R
    
    note right of R
        rotation_input
    end note
    
    R --> ROTATE
    
    note right of ROTATE
        adjust_grain
    end note
    
    ROTATE --> check_completion
    
    mode_syntax_break --> X
    
    note right of X
        FAILED
    end note
    
    X --> [*]
```

EXAMPLE: COFFEE WITH CATEGORICAL STRUCTURE (Complete Domain Integration)
==========================================================================

STEP 1: VENDOR DOMAIN PRIMITIVES
---------------------------------

THERMODYNAMICS Domain:
```mermaid
stateDiagram-v2
    [*] --> S_vendor_thermo
    S_vendor_thermo --> S_arrhenius
    S_vendor_thermo --> S_newton
    S_vendor_thermo --> S_heat_cap
    
    note right of S_arrhenius
        Arrhenius rate
        k = A·e^(-Ea/RT)
        dissolution rate vs temperature
    end note
    
    note right of S_newton
        Newton cooling
        dT/dt = -h·A·(T-T_env)
        heat transfer rate
    end note
    
    note right of S_heat_cap
        Specific heat
        Q = m·c·ΔT
        energy required
    end note
```

EXTRACTION_KINETICS Domain:
```mermaid
stateDiagram-v2
    [*] --> S_vendor_kinetics
    S_vendor_kinetics --> S_ficks
    S_vendor_kinetics --> S_yield
    S_vendor_kinetics --> S_partition
    S_vendor_kinetics --> S_surface
    
    note right of S_ficks
        Fick's law
        J = -D·(dC/dx)
        mass transport by diffusion
    end note
    
    note right of S_yield
        Yield curve
        Y(t) = Y_max·(1 - e^(-k·t))
        Y_max ≈ 28-30% (physical limit)
        Target: 18-22% (optimal taste)
    end note
    
    note right of S_partition
        Partition coef
        K = C_coffee/C_water
        equilibrium concentration
    end note
    
    note right of S_surface
        Surface area
        A ~ 1/d_particle
        grind size affects contact area
    end note
```

FLUID_DYNAMICS Domain:
```mermaid
stateDiagram-v2
    [*] --> S_vendor_fluid
    S_vendor_fluid --> S_flow
    S_vendor_fluid --> S_contact
    S_vendor_fluid --> S_channel
    
    note right of S_flow
        Flow rate
        Q = A·v
        water delivery rate
    end note
    
    note right of S_contact
        Contact time
        t_contact = V_bed/Q
        exposure duration
    end note
    
    note right of S_channel
        Channeling
        δ = σ(v)/mean(v)
        flow uniformity metric
    end note
```

STEP 2: TOWER COMPOSITION
--------------------------

COFFEE_TOWER (Complete Function Set):
```mermaid
stateDiagram-v2
    [*] --> L1_physical
    
    state "L1: Physical Parameters" as L1_physical {
        [*] --> S_inputs
        S_inputs --> S_mass_coffee
        S_inputs --> S_mass_water
        S_inputs --> S_temp_initial
        S_inputs --> S_grind_size
        
        S_mass_coffee --> S_compute_bed
        S_grind_size --> S_compute_surface
        S_compute_surface --> S_interface_area
        S_compute_bed --> S_bed_volume
        
        note right of S_interface_area
            A ~ m_coffee / d_grind
            Determines contact area
        end note
    }
    
    L1_physical --> L2_chemistry: TOWER[EXT thermodynamics + extraction_kinetics]
    
    state "L2: Chemistry (Dissolution Dynamics)" as L2_chemistry {
        [*] --> S_rate_equation
        
        note right of S_rate_equation
            dC/dt = k(T)·A·(C_sat(T) - C(t))
            
            where:
            k(T) = A·e^(-Ea/RT)  [Arrhenius]
            C_sat(T) = K·C_coffee [Partition]
            A = surface_area(d_grind)
        end note
        
        S_rate_equation --> S_concentration_profile
        S_concentration_profile --> S_compound_extraction
        
        note right of S_compound_extraction
            Extracts: caffeine, oils, acids, aromatics
            Over-extraction: bitter tannins
            Optimal window: 18-22% yield
        end note
    }
    
    L2_chemistry --> L3_process: TOWER[EXT fluid_dynamics]
    
    state "L3: Process Control (Extraction Trajectory)" as L3_process {
        [*] --> S_flow_control
        S_flow_control --> S_residence_calc
        
        note right of S_residence_calc
            t_contact = V_bed/Q
            Q = flow_rate(pour_pattern)
        end note
        
        S_residence_calc --> S_integrate_yield
        
        note right of S_integrate_yield
            Y_total(t) = ∫[0,t] (dC/dt)·Q·dt / m_coffee
            
            Target: 18% ≤ Y ≤ 22%
            Typical t: 2-4 minutes
        end note
        
        S_integrate_yield --> S_quality_check
    }
    
    L3_process --> L4_metaprogram: TOWER[abstract]
    
    state "L4: Metaprogram (Complete Function)" as L4_metaprogram {
        [*] --> S_function_signature
        
        note right of S_function_signature
            Coffee: (m_coffee, m_water, T, d_grind, t, Q) 
                 → (Y_pct, C_final, quality_score)
            
            Compose: L3 ∘ L2 ∘ L1
            
            Optimization:
            • T_optimal: 92-96°C (max k without over-extraction)
            • d_grind: 0.5-0.75mm (balance A vs channeling)
            • t_contact: 2-4min (reach target before bitters)
            • Q: slow_steady (minimize channeling δ)
        end note
        
        S_function_signature --> S_executable
        S_executable --> [*]
    }
    
    L4_metaprogram --> [*]
```

STEP 3: OPERATIONAL GRAPH WITH REAL EXT CONNECTIONS
----------------------------------------------------

BREW_FRENCH_PRESS (Domain-Integrated):
```mermaid
stateDiagram-v2
    [*] --> S_setup
    
    note right of S_setup
        m_coffee=18g, m_water=288g
        T_target=95C, d_grind=0.6mm
    end note
    
    S_setup --> S_heat_water
    S_heat_water --> S_water_ready: EXT[thermodynamics.heat_transfer]
    
    note right of S_water_ready
        T=95C
        Extension to @{THERMODYNAMICS.Newton_cooling}:
        Heat until dT/dt ≈ 0 at T_target
        Q_required = m·c·ΔT = 288g × 4.18J/g°C × 75°C ≈ 90kJ
    end note
    
    S_water_ready --> S_add_grounds
    S_add_grounds --> S_pour_water
    S_pour_water --> S_start_extraction
    
    S_start_extraction --> S_steep_timer: EXT[extraction_kinetics.yield_curve]
    
    note right of S_steep_timer
        t=0, target=240s
        Extension to @{EXTRACTION_KINETICS.yield_curve}:
        Y(t) = 28%·(1 - e^(-k·t))
        k ≈ 0.012/s at T=95°C, d=0.6mm
        Y(240s) ≈ 19.5% ✓ (in optimal 18-22% range)
        
        WHY 240s? Because that's where the yield curve
        reaches target extraction without over-extraction
    end note
    
    S_steep_timer --> T
    state T <<choice>>
    T --> S_wait: [t < 240]
    T --> S_extraction_complete: [t >= 240]
    
    note right of S_wait
        t++
    end note
    
    S_wait --> S_steep_timer
    
    S_extraction_complete --> CHECK
    state CHECK <<choice>>
    
    note right of CHECK
        Checking: domain=coffee_making, grain=observable
        Domain check: ✓ (coffee making)
        Grain check: Are we at observable level?
        
        CORRECT: temp, time, measurements
        ORTHOGONAL: molecular formulas, equations
        SYNTAX_BREAK: wrong domain entirely
    end note
    
    CHECK --> S_plunge: [CORRECT]
    CHECK --> ROTATE: [ORTHOGONAL]
    
    note right of ROTATE
        grain=molecular→observable
    end note
    
    ROTATE --> S_restate_observable
    S_restate_observable --> S_plunge
    
    S_plunge --> S_pour
    S_pour --> S_done: COLLAPSE[physical, quotient=0]
    
    note right of S_done
        COLLAPSE verification:
        Required observables: [temp, time, color, aroma, volume]
        Provided observables: [95°C, 240s, dark brown, aromatic, 288ml]
        quotient = 0 ✓
        
        Circuit fully grounded to physical substrate
    end note
    
    S_done --> [*]
```

STEP 4: VERIFICATION OF CATEGORICAL STRUCTURE
----------------------------------------------

Extension Connections Verified:
• S_water_ready --> via EXT[thermodynamics] --> @{Newton_cooling, Arrhenius_rate}
• S_steep_timer --> via EXT[extraction_kinetics] --> @{yield_curve, Ficks_law}
• S_extraction --> via EXT[fluid_dynamics] --> @{residence_time, flow_rate}

Tower Composition Verified:
• L1 (physical) → L2 (chemistry) → L3 (process) → L4 (metaprogram)
• Each level composes functions from lower levels
• L4 is the complete reified circuit

Collapse Verification:
• Started at L4 (abstract metaprogram)
• Collapsed through L3 (process equations)
• Collapsed through L2 (chemical rates)  
• Reached L1 (physical observables: 95°C, 240s, 18g, 288g)
• quotient = 0 ✓

The metaprogram IS the latent circuit, explicitly constructed by
composing domain functions through the categorical tower.

EXTENSION EXAMPLES (How EXT Marks Connect to Vendored Domains)
================================================================

Example 1: Temperature → Thermodynamics
----------------------------------------
User asks: "Why 95°C specifically?"

Surface graph says:
```
S_heat_water --> S_water_ready
```

EXT expansion via EXT[thermodynamics, grain=practical]:
```mermaid
stateDiagram-v2
    S_water_ready --> expanded_arrhenius: EXT[thermodynamics.Arrhenius_rate]
    
    note right of expanded_arrhenius
        k(T) = A·e^(-Ea/RT)
        
        At T=95°C (368K): k ≈ 0.012/s (optimal extraction rate)
        At T=85°C (358K): k ≈ 0.006/s (too slow, under-extraction)
        At T=100°C (373K): k ≈ 0.018/s (too fast, bitter tannins extract)
        
        Result: 92-96°C gives max extraction rate for desired compounds
                without triggering bitter compound extraction
    end note
    
    expanded_arrhenius --> collapsed: COLLAPSE[observable]
    
    note right of collapsed
        "Heat to 95°C for optimal extraction speed"
    end note
```

The EXT mark points to the actual Arrhenius equation in the vendored thermodynamics domain, which explains WHY 95°C is optimal.

Example 2: Steeping → Extraction Kinetics
------------------------------------------
User asks: "Why 240 seconds?"

Surface graph says:
```
S_steep_timer[target=240s]
```

EXT expansion via EXT[extraction_kinetics, grain=observable]:
```mermaid
stateDiagram-v2
    S_steep_timer --> expanded_yield: EXT[extraction_kinetics.yield_curve]
    
    note right of expanded_yield
        Y(t) = Y_max·(1 - e^(-k·t))
        Y_max ≈ 28% (physical limit at these conditions)
        k ≈ 0.012/s (from Arrhenius at T=95°C)
        
        Y(180s) = 28%·(1 - e^(-0.012·180)) ≈ 16.8% (under-extracted)
        Y(240s) = 28%·(1 - e^(-0.012·240)) ≈ 19.5% (optimal) ✓
        Y(300s) = 28%·(1 - e^(-0.012·300)) ≈ 21.8% (approaching over-extraction)
        
        Target range: 18-22% for balanced flavor
        Result: 240s hits middle of optimal window
    end note
    
    expanded_yield --> collapsed: COLLAPSE[observable]
    
    note right of collapsed
        "Steep for 4 minutes to reach 19-20% extraction"
    end note
```

The EXT mark points to the actual yield curve function, which shows that 240s puts you in the optimal extraction window.

Example 3: Grind Size → Surface Area
-------------------------------------
User asks: "Why medium grind?"

Surface graph says:
```
S_grind[size=medium]
```

EXT expansion via EXT[extraction_kinetics.surface_area]:
```mermaid
stateDiagram-v2
    S_grind --> expanded_surface: EXT[extraction_kinetics.surface_area + fluid_dynamics.channeling]
    
    note right of expanded_surface
        Surface area: A ~ m_coffee / d_particle
        Channeling: δ = σ(v)/mean(v)
        
        Fine grind (d=0.3mm):
          A_interface ≈ 60 cm²/g (high)
          δ_channeling ≈ 0.4 (high variance, uneven extraction)
          Result: fast extraction but inconsistent, some areas over-extracted
        
        Medium grind (d=0.6mm):
          A_interface ≈ 30 cm²/g (moderate) ✓
          δ_channeling ≈ 0.15 (low variance) ✓
          Result: balanced extraction rate with uniform flow
        
        Coarse grind (d=1.2mm):
          A_interface ≈ 15 cm²/g (low)
          δ_channeling ≈ 0.1 (very uniform)
          Result: too slow, under-extraction even at long times
    end note
    
    expanded_surface --> collapsed: COLLAPSE[observable]
    
    note right of collapsed
        "Use medium grind for balanced extraction without channeling"
    end note
```

The EXT mark points to TWO vendored functions (surface area AND channeling) that together explain why medium grind is optimal.

Example 4: Orthogonal Completion Detection
-------------------------------------------
LLM generates at wrong grain:

```
OUTPUT: "The caffeol molecules (C₈H₁₀O) undergo dipole-induced dipole 
interactions with H₂O molecules. The London dispersion forces contribute
ΔG ≈ -2.3 kJ/mol to the dissolution free energy..."
```

CHECK execution:
```mermaid
stateDiagram-v2
    S_molecular_output --> CHECK
    
    note right of CHECK
        Domain check: ✓ (extraction_kinetics.partition_coef referenced)
        Grain check: ✗ (molecular formulas, ΔG values = L2 grain)
        Required grain: L0 (observable)
        
        Result: ORTHOGONAL
        Distance: |L2 - L0| = 2 grain levels
    end note
    
    CHECK --> ORTHOGONAL_detected
```

User feedback: "I just want to know what's happening that I can see."

ROTATE execution:
```mermaid
stateDiagram-v2
    ORTHOGONAL_detected --> apply_rotate: ROTATE[grain from L2_molecular to L0_observable]
    
    note right of apply_rotate
        Must reduce distance by ≥1 per ROTATE
        Target: observable effects only
        
        Re-generate using same domain (extraction_kinetics) but L0 grain:
        
        OUTPUT: "Hot water dissolves coffee oils and caffeine from the grounds.
        You can see this as the water darkens and develops aroma. The longer
        it steeps, the more compounds extract, changing the color from light
        brown to dark brown."
    end note
    
    apply_rotate --> CHECK2
    CHECK2 --> CORRECT: domain match, grain match
    
    note right of CORRECT
        COLLAPSE: quotient=0 (all observable: color, aroma, time)
    end note
```

Example 5: Tower Navigation
----------------------------
User asks: "Can you show me the math?"

Current grain: L0 (observable)
Request: Show L2 (mathematical)

TOWER operation:
```mermaid
stateDiagram-v2
    S_steep_observable --> tower_up: TOWER[L0 to L2 extract_theory]
    
    note right of S_steep_observable
        Current state: "4 minutes"
    end note
    
    tower_up --> S_mathematics
    
    note right of S_mathematics
        Y(t) = Y_max·(1 - e^(-k·t))
        k = A·e^(-Ea/RT)
        J = -D·(dC/dx)
        
        User can now see the equations behind "4 minutes"
    end note
    
    S_mathematics --> tower_down: TOWER[L2 to L0 COLLAPSE observable]
    
    tower_down --> S_steep_practical
    
    note right of S_steep_practical
        "Based on those equations, steep for 4 minutes"
    end note
```

The TOWER operator lets you navigate UP to see theory or DOWN to ground in observables, while maintaining the same domain (extraction_kinetics).

GRANULARITY LEVELS
==================

For Coffee Domain:
L0: Physical/Observable
    - Temperature readings
    - Time durations  
    - Color changes
    - Taste qualities
    
L1: Chemical/Process
    - Compound extraction
    - Solubility rates
    - Concentration gradients
    
L2: Molecular/Structural
    - Specific molecules (caffeol, caffeine)
    - Chemical bonds
    - Reaction mechanisms
    
L3: Quantum/Fundamental
    - Electron orbitals
    - Quantum interactions
    - Wave functions

COLLAPSE rules:
- Coffee making: collapse to L0 (observable)
- Coffee science: collapse to L1 (chemical)
- Research paper: collapse to L2 (molecular)
- Theoretical chemistry: stay at L3 (quantum)

The quotient at each level:
- quotient=0: fully instantiated at that grain
- quotient>0: still abstract, need more collapse

SELF-HOSTING PROOF
==================

The categorical system describes itself:

CATEGORICAL_SYSTEM_GRAPH:
```mermaid
stateDiagram-v2
    [*] --> define_primitives
    define_primitives --> primitive_defs
    
    note right of primitive_defs
        @{PRIMITIVE_DEFINITIONS}
    end note
    
    primitive_defs --> categorical_extensions: EXT[category_theory, grain=practical]
    
    note right of categorical_extensions
        This very system uses:
        - EXT to mark domain transitions
        - TOWER to show abstraction
        - COLLAPSE to ground explanations
        - CHECK to validate completions
        - ROTATE to fix orthogonality
    end note
    
    categorical_extensions --> meta_graph
    
    note right of meta_graph
        @{META_GRAPH}
    end note
    
    meta_graph --> verify_self_hosting
    
    verify_self_hosting --> CHECK
    state CHECK <<choice>>
    CHECK --> closure: [uses own notation]
    CHECK --> X: [does not use own notation]
    
    note right of X
        incomplete
    end note
    
    closure --> S_complete
    
    note right of S_complete
        System is self-describing
    end note
    
    S_complete --> [*]
```

Closure condition: Every graph in the system (including this one) 
uses only primitives defined within the system.

✓ VERIFIED: This document is written in its own notation.

USAGE GUIDELINES
================

When to use EXT:
- User asks "why?" about a step
- Causal mechanism is in adjacent domain
- Explanation requires domain shift

When to use COLLAPSE:
- Abstract reasoning must ground to physical
- User needs concrete/observable output
- Preventing infinite abstraction tower

When to use ROTATE:
- LLM gives correct domain, wrong granularity
- "Cat has follicles" vs "Cat has fur color"
- User signals: "too detailed" or "too abstract"

When to use CHECK:
- After any complex generation
- Verify domain and grain match requirements
- Detect orthogonal vs correct vs broken

COMPLETE EXAMPLE: Making Coffee with Full Annotations
======================================================

User: "Make me coffee"

PROCESS:
1. Request received → tower to beverage_preparation domain
2. Check grounding requirement → must collapse to physical actions
3. Generate coffee graph at L0 (observable/physical)
4. Mark EXT points for potential chemistry/physics expansion
5. Include CHECK for completion verification
6. Output with collapse confirmed

If LLM outputs molecular details:
→ CHECK detects orthogonal (chemistry domain ✓, but grain=molecular not observable)
→ User: "I just want to make coffee, not a chemistry lecture"
→ ROTATE[grain from molecular to observable]
→ Corrected output at physical action level

This notation is:
- Turing complete (via S,T,R,W,B,L,@,X)
- Categorically structured (via EXT,COLLAPSE,TOWER,ROTATE,CHECK)
- Self-hosting (describes itself in its own notation)
- Domain-traversing (EWS tower navigation)
- Orthogonality-detecting (completion mode checking)
- Granularity-aware (quotient class specifications)

═══════════════════════════════════════════════════════════
END OF CATEGORICAL STATE GRAPH NOTATION v1.0
═══════════════════════════════════════════════════════════

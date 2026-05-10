# Current Module Map

Generated from `mbse_core.module_registry`.

## Mermaid Diagram

```mermaid
flowchart LR
    subgraph initial_sizing_node["initial_sizing"]
        direction LR
        initial_sizing_inputs["Inputs"]
        initial_sizing_in_1["InitialSizingInputs"]
        initial_sizing_in_1 --> initial_sizing_inputs
        initial_sizing_in_2["InitialSizingAircraftInputs"]
        initial_sizing_in_2 --> initial_sizing_inputs
        initial_sizing_in_3["MissionSegmentInput"]
        initial_sizing_in_3 --> initial_sizing_inputs
        initial_sizing_body["initial_sizing<br/>implemented_low_fidelity<br/>domains.initial_sizing"]
        initial_sizing_outputs["Outputs"]
        initial_sizing_out_1["InitialSizingOutputs"]
        initial_sizing_outputs --> initial_sizing_out_1
        initial_sizing_out_2["SegmentSizingResult"]
        initial_sizing_outputs --> initial_sizing_out_2
        initial_sizing_out_3["converged_takeoff_weight_lb"]
        initial_sizing_outputs --> initial_sizing_out_3
        initial_sizing_out_4["fuel_fraction"]
        initial_sizing_outputs --> initial_sizing_out_4
        initial_sizing_out_5["structure_fraction"]
        initial_sizing_outputs --> initial_sizing_out_5
        initial_sizing_inputs --> initial_sizing_body
        initial_sizing_body --> initial_sizing_outputs
    end
    subgraph constraint_analysis_node["constraint_analysis"]
        direction LR
        constraint_analysis_inputs["Inputs"]
        constraint_analysis_in_1["ConstraintAnalysisInputs"]
        constraint_analysis_in_1 --> constraint_analysis_inputs
        constraint_analysis_in_2["ConstraintScenarioInput"]
        constraint_analysis_in_2 --> constraint_analysis_inputs
        constraint_analysis_in_3["wing_loading_values_lb_per_ft2"]
        constraint_analysis_in_3 --> constraint_analysis_inputs
        constraint_analysis_in_4["maximum_thrust_lb"]
        constraint_analysis_in_4 --> constraint_analysis_inputs
        constraint_analysis_in_5["military_thrust_lb"]
        constraint_analysis_in_5 --> constraint_analysis_inputs
        constraint_analysis_body["constraint_analysis<br/>implemented_low_fidelity<br/>domains.constraint_analysis"]
        constraint_analysis_outputs["Outputs"]
        constraint_analysis_out_1["ConstraintAnalysisOutputs"]
        constraint_analysis_outputs --> constraint_analysis_out_1
        constraint_analysis_out_2["ConstraintCurveResult"]
        constraint_analysis_outputs --> constraint_analysis_out_2
        constraint_analysis_out_3["envelope_thrust_to_weight"]
        constraint_analysis_outputs --> constraint_analysis_out_3
        constraint_analysis_out_4["selected_wing_loading_lb_per_ft2"]
        constraint_analysis_outputs --> constraint_analysis_out_4
        constraint_analysis_out_5["selected_thrust_to_weight"]
        constraint_analysis_outputs --> constraint_analysis_out_5
        constraint_analysis_inputs --> constraint_analysis_body
        constraint_analysis_body --> constraint_analysis_outputs
    end
    initial_sizing_outputs -->|downstream| constraint_analysis_inputs
```

## Registered Modules

### initial_sizing

- Package: `domains.initial_sizing`
- Status: `implemented_low_fidelity`
- Purpose: Run MaCa-style low-fidelity mission fuel fraction and takeoff weight convergence.
- Inputs: InitialSizingInputs, InitialSizingAircraftInputs, MissionSegmentInput
- Outputs: InitialSizingOutputs, SegmentSizingResult, converged_takeoff_weight_lb, fuel_fraction, structure_fraction
- Downstream modules: constraint_analysis

### constraint_analysis

- Package: `domains.constraint_analysis`
- Status: `implemented_low_fidelity`
- Purpose: Evaluate MaCa-style thrust-loading versus wing-loading constraint curves and select a low-fidelity design point.
- Inputs: ConstraintAnalysisInputs, ConstraintScenarioInput, wing_loading_values_lb_per_ft2, maximum_thrust_lb, military_thrust_lb
- Outputs: ConstraintAnalysisOutputs, ConstraintCurveResult, envelope_thrust_to_weight, selected_wing_loading_lb_per_ft2, selected_thrust_to_weight
- Downstream modules: (none)

## Regenerating This Diagram

From the repository root, run:

```bash
python3 scripts/generate_module_diagram.py
```

The script reads `mbse_core.module_registry` as the source of truth and rewrites this Markdown file.

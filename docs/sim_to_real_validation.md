# Sim-to-Real Validation Record

Keep simulated results separate from physical measurements.

| Parameter | Simulation baseline | Hardware value |
|---|---|---|
| Wheel radius | 0.032 m model default | Measure |
| Wheel separation | 0.21 m nominal baseline | Measure |
| Sensor update rate | 10 Hz model default | Measure |
| Obstacle threshold | 0.35 m controller default | Tune and record |
| Stopping distance | Measure in simulation | Measure safely |
| Turn response | Measure in simulation | Measure |
| Battery voltage under load | N/A | Measure |

## Procedure
1. Confirm the robot spawns and scan values are finite.
2. Verify invalid scan data causes zero velocity.
3. Verify an obstacle triggers a turn.
4. Measure repeated straight-line and turn trials.
5. On hardware, start with wheels raised, low speed and an accessible power disconnect.
6. Record setup, uncertainty and differences between simulation and hardware.

The URDF is a simplified geometry model. Wheel friction, motor torque curve, battery sag, driver deadband, caster drag and sensor noise are not calibrated to a physical chassis by default.

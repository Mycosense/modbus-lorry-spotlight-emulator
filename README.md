# modbus-lorry-spotlight-emulator

## Install the project

```bash
# If you use venv
python3 -m venv venv
source ./venv/bin/activate

# Install the package
pip install -U setuptools # only for python 3.10
pip install -e .
```

## Run the emulator

If you want to emulate the spotlight as device on the modbus. You can run the following script:

```bash
emulate_spotlight
```

## Power ON sequence
```mermaid
sequenceDiagram
    actor Picker
    participant L as Lorry
    participant S as Spotlight
    Note over Picker,S: Power ON sequence
    Picker->>+L: Lorry power ON
    loop Every 800ms
        L->>S: Req: "spotlight_control_enable" (no resp.)
    end
    L->>+S: Spotlight Power ON
    S->>-S: Boot 30sec
    activate L
    L->>+S: Req: "spotlight_control_enable"
    S->>-L: Resp: "spotlight_control_enable = H" 
    L->>L: Display status "spotlight ready"
    deactivate L
```

## Start moving from picker

```mermaid
sequenceDiagram
    actor Picker
    participant L as Lorry
    participant S as Spotlight
    Note over Picker,S: Starting moving from picker
    activate L
    Picker->>+L: Start Lorry (either direction)
    L->>L: "spotlight_suggestion_mode" = H 
    loop Every 800ms
        activate S
        L->>S: Req: "spotlight_control_enable"
        S->>L: Resp: "spotlight_control_enable" = H (enable)
        L->>L: If "spotlight_control_enable" == H, then continue
        S->>S: Adjust speed
        L->>S: Request "spotlight_speed"
        S->>L: Respond "spotlight_speed"
        L->>L: Adjust speed
        L->>S: Send lorry status (full Holding register)
        deactivate S
    end
    deactivate L
```

## Disable spotlight speed from spotlight
```mermaid
sequenceDiagram
    actor Picker
    participant L as Lorry
    participant S as Spotlight
    Note over Picker,S: Disable form spotlight
    activate L
    S->>S: "spotlight_control_enable" = L
    activate S
    L->>S: Req: "spotlight_control_enable"
    S->>L: Resp: "spotlight_control_enable" = L
    L->>L: If "spotlight_control_enable" == L, then stop
    L->>L: Stop motor
    loop Every 800ms
        L->>S: Send lorry status (full Holding register)
        L->>S: Req: "spotlight_control_enable"
    S->>L: Resp: "spotlight_control_enable" = L
    end
    deactivate S
    deactivate L
```

## Stop lorry from picker
```mermaid
sequenceDiagram
    actor Picker
    participant L as Lorry
    participant S as Spotlight
    Note over Picker,S: Stop lorry form picker
    activate L
    Picker->>+L: Stop Lorry
    L->>L: "spotlight_suggestion_mode" = L 
    L->>L: Stop motor
    loop Every 800ms
        activate S
        L->>S: Send lorry status (full Holding register)
        deactivate S
    end
    deactivate L
```

## Adjust lorry speed from picker
```mermaid
sequenceDiagram
    actor Picker
    participant L as Lorry
    participant S as Spotlight
    Note over Picker,S: Manual speed form picker
    activate L
    Picker->>+L: Change speed of Lorry manually
    L->>L: "spotlight_suggestion_mode" = L 
    L->>L: Adjust speed
    loop Every 800ms
        activate S
        L->>S: Send lorry status (full Holding register)
        deactivate S
    end
    deactivate L
```
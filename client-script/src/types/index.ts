export enum TestRecorderState {
    IDLE = "IDLE",
    LOADING = "LOADING",
    RECORDING = "RECORDING",
}

export enum TestState {
    INITIALIZING = "INITIALIZING",
    RUNNING = "RUNNING",
    COMPLETED = "COMPLETED",
    FAILED = "FAILED",
}

export enum TestFrequency {
    DAILY = "DAILY",
    WEEKLY = "WEEKLY",
}

export const TestFrequencyOptions = Object.values(TestFrequency);

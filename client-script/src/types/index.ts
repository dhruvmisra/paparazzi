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

export type CreateTestRequest = {
    name: string;
    frequency: TestFrequency;
    baseUrl: string;
    device: DeviceInfo;
};

export type DeviceInfo = {
    ua: string;
};

export type CreateTestResponse = CreateTestRequest & {
    id: string;
    createdAt: string;
    state: TestState;
};

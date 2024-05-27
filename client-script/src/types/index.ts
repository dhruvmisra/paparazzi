export enum TestRecorderState {
    IDLE = "IDLE",
    LOADING = "LOADING",
    RECORDING = "RECORDING",
    FAILED = "FAILED",
}

export enum TestState {
    RECORDING = "RECORDING",
    RECORDED = "RECORDED",
}

export enum TestFrequency {
    DAILY = "DAILY",
    WEEKLY = "WEEKLY",
}

export enum TestStepType {
    CLICK = "CLICK",
    NAVIGATION = "NAVIGATION",
    SCROLL = "SCROLL",
    SCREENSHOT = "SCREENSHOT",
}

export const TestFrequencyOptions = Object.values(TestFrequency);

// Test
export type CreateTestRequest = {
    name: string;
    frequency: TestFrequency;
    baseUrl: string;
    device: DeviceInfo;
};

export type DeviceInfo = {
    ua: string;
    viewport: Viewport;
};

export type Viewport = {
    width: number;
    height: number;
};

export type Test = CreateTestRequest & {
    id: string;
    createdAt: string;
    state: TestState;
};

export type TestParams = {
    testId: string;
};

// TestStep
export type TestStep = {
    id: string;
    testId: string;
    createdAt: string;
    type: TestStepType;
    location?: {
        url: string;
    };
    clickPosition?: {
        x: number;
        y: number;
    };
    scrollPosition?: {
        x: number;
        y: number;
    };
    screenshotPath?: string;
};

import { BACKEND_URL, USER_ID } from "../config";
import { TestStep, TestStepType } from "../types";
import { generateTestStepId, takeScreenshot } from "../utils";

export const constructClickStep = (testId: string, event: MouseEvent): TestStep => {
    const step: TestStep = {
        id: generateTestStepId(),
        createdAt: new Date().toISOString(), // TODO: change this to server_time
        testId: testId,
        type: TestStepType.CLICK,
        clickPosition: {
            x: event.clientX,
            y: event.clientY,
        },
    };
    return step;
};

export const constructScrollStep = (testId: string, _event: Event): TestStep => {
    const step: TestStep = {
        id: generateTestStepId(),
        createdAt: new Date().toISOString(), // TODO: change this to server_time
        testId: testId,
        type: TestStepType.SCROLL,
        scrollPosition: {
            x: window.scrollX,
            y: window.scrollY,
        },
    };
    return step;
};

export const constructNavigationStep = (testId: string, url: string): TestStep => {
    const step: TestStep = {
        id: generateTestStepId(),
        createdAt: new Date().toISOString(), // TODO: change this to server_time
        testId: testId,
        type: TestStepType.NAVIGATION,
        location: {
            url: url,
        },
    };
    return step;
};

export const constructScreenshotStep = (testId: string): TestStep => {
    const step: TestStep = {
        id: generateTestStepId(),
        createdAt: new Date().toISOString(), // TODO: change this to server_time
        testId: testId,
        type: TestStepType.SCREENSHOT,
    };
    return step;
};

export const CreateTestStep = async (testStep: TestStep) => {
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testStep.testId}/steps`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-user-id": USER_ID,
        },
        body: JSON.stringify(testStep),
    });

    return response.json() as Promise<TestStep>;
};

export const CreateTestStepScreenshot = async (testId: string, testStepId: string, screenshotFile: File) => {
    const data = new FormData();
    data.append("file", screenshotFile);

    const response = await fetch(`${BACKEND_URL}/v1/tests/${testId}/steps/${testStepId}/screenshots`, {
        method: "POST",
        headers: {
            "x-user-id": USER_ID,
        },
        body: data,
    });

    return response.json();
};

export const TakeScreenshotAndCreateStep = async (testId: string) => {
    const step = constructScreenshotStep(testId);
    await CreateTestStep(step);
    const screenshotFile = await takeScreenshot();
    await CreateTestStepScreenshot(testId, step.id, screenshotFile);
};

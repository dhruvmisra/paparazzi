import { BACKEND_URL } from "../config";
import { TestFrequency, CreateTestRequest, Test, TestState } from "../types";

export const CheckHealth = async () => {
    const response = await fetch(`${BACKEND_URL}/v1/health`);
    return response.json();
};

export const CreateTest = async (name: string, frequency: TestFrequency) => {
    const body: CreateTestRequest = {
        name,
        frequency,
        baseUrl: window.location.origin,
        device: {
            ua: navigator.userAgent,
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight,
            },
        },
    };

    const response = await fetch(`${BACKEND_URL}/v1/tests`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    return response.json() as Promise<Test>;
};

export const GetTest = async (testId: string) => {
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testId}`);
    return response.json() as Promise<Test>;
};

export const CompleteTest = async (testId: string) => {
    const body = {
        state: TestState.RECORDED
    }
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    return response.json() as Promise<Test>;
}


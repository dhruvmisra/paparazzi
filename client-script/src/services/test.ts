import { BACKEND_URL, USER_ID } from "../config";
import { TestFrequency, CreateTestRequest, Test } from "../types";

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
            "x-user-id": USER_ID
        },
        body: JSON.stringify(body),
    });

    return response.json() as Promise<Test>;
};

export const GetTest = async (testId: string) => {
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testId}`, {
        headers: {
            "x-user-id": USER_ID
        }
    });
    return response.json() as Promise<Test>;
};

export const CompleteTest = async (testId: string) => {
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testId}/complete`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-user-id": USER_ID
        }
    });

    return response.json() as Promise<Test>;
}


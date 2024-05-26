import { BACKEND_URL } from "../config";
import { TestStep } from "../types";

export const CreateTestStep = async (testStep: TestStep) => {
    const response = await fetch(`${BACKEND_URL}/v1/tests/${testStep.testId}/steps`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(testStep),
    });

    return response.json() as Promise<TestStep>;
};

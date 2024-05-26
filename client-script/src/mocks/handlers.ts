import { http, HttpResponse } from "msw";
import { BACKEND_URL } from "../config";
import { CreateTestRequest, Test, TestFrequency, TestParams, TestState, TestStep } from "../types";
import { generateTestId, generateTestStepId } from "../utils";

export const handlers = [
    http.get(BACKEND_URL + "/v1/health", () => {
        return HttpResponse.json({ message: "OK" });
    }),

    http.post<{}, CreateTestRequest, Test>(`${BACKEND_URL}/v1/tests`, async ({ request }) => {
        const req = await request.json();
        const res = {
            id: generateTestId(),
            createdAt: new Date().toISOString(),
            state: TestState.RUNNING,
            name: req.name,
            frequency: req.frequency,
            baseUrl: req.baseUrl,
            device: req.device,
        };
        return HttpResponse.json(res);
    }),

    http.get<TestParams, {}, Test>(`${BACKEND_URL}/v1/tests/:testId`, async ({ params }) => {
        const { testId } = params;
        const res = {
            id: testId,
            createdAt: new Date().toISOString(),
            state: TestState.RUNNING,
            name: "Dummy test",
            frequency: TestFrequency.DAILY,
            baseUrl: "http://localhost:5173",
            device: {
                ua: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport: {
                    height: 1080,
                    width: 1920,
                },
            },
        };
        return HttpResponse.json(res);
    }),

    http.post<TestParams, TestStep, TestStep>(`${BACKEND_URL}/v1/tests/:testId/steps`, async ({ request }) => {
        const req = await request.json();
        const res = {
            id: generateTestStepId(),
            createdAt: new Date().toISOString(),
            testId: req.testId,
            type: req.type,
            location: req.location,
            scrollPosition: req.scrollPosition,
            clickPosition: req.clickPosition,
            screenshotPath: req.screenshotPath,
        };
        return HttpResponse.json(res);
    }),
];

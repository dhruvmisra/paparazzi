import { http, HttpResponse } from "msw";
import { BACKEND_URL } from "../config";
import { CreateTestRequest, CreateTestResponse, TestFrequency, TestState } from "../types";

export const handlers = [
  http.get(BACKEND_URL + "/v1/health", () => {
    return HttpResponse.json({ message: "OK" });
  }),
  
  http.post<{}, CreateTestRequest, CreateTestResponse>(`${BACKEND_URL}/v1/tests`, async ({ request }) => {
    const req = await request.json();
    const res = {
      id: "test-" + Math.random().toString(36).substring(2),
      createdAt: new Date().toISOString(),
      state: TestState.RUNNING,
      name: req.name,
      frequency: req.frequency,
      baseUrl: req.baseUrl,
      device: req.device,
    };
    return HttpResponse.json(res);
  }),
  
  http.get<{ testId: string }, {}, CreateTestResponse>(`${BACKEND_URL}/v1/tests/:testId`, async ({ params }) => {
    const { testId } = params;
    const res = {
      id: testId,
      createdAt: new Date().toISOString(),
      state: TestState.RUNNING,
      name: "",
      frequency: TestFrequency.DAILY,
      baseUrl: "http://localhost:5173",
      device: {
        ua: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
      }
    };
    return HttpResponse.json(res);
  }),
];

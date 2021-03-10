from locust import HttpUser, task


class reportService(HttpUser):
    
    def generate_report(self):
        resp = self.client.post("report")
        if resp.status_code != 200:
            print("Error generating report")
        return resp
    
    def check_status(self,id):
        while(True):
            print(id)
            resp = self.client.get(f"report/{id}")
            resp = resp.json()
            print(resp)
            if "result" in resp.keys():
                if resp["result"]!= None:
                    if resp["result"]["state"] == "completed":
                        return resp

    
    @task
    def complete_flow(self):
        resp = self.generate_report()
        resp = resp.json()
        output = self.check_status(resp["report_id"])
        print("done")
    
    @task
    def generate_flow(self):
        self.generate_report()

    

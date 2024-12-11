class ClimateModel:
    def __init__(self):
        # Global parameters
        self.params = {
            "policy": None,
            "impact": "off",
            "savings": "off",
            "cooperation": "off",
            "burden_share": "equal_per_capita",
            "ctax_initial": 0,
            "cbudget": None,
            "tatm_limit": None,
            "carbon_debt": False
        }

    def set_policy(self, policy):
        valid_policies = ["BAU", "CBudget", "CEA", "CTax", "Simulation"]
        if policy not in valid_policies:
            raise ValueError(f"Invalid policy: {policy}")
        self.params["policy"] = policy

    def configure_params(self):
        policy = self.params["policy"]
        if policy == "BAU":
            self.params.update({
                "impact": "off",
                "savings": "off",
                "cooperation": "off"
            })
        elif policy == "CBudget":
            self.params.update({
                "impact": "on",
                "savings": "on",
                "cooperation": "on"
            })
            if self.params["cbudget"] is None:
                raise ValueError("Carbon budget (cbudget) must be specified for CBudget policy!")
        elif policy == "CEA":
            self.params.update({
                "impact": "on",
                "savings": "on",
                "cooperation": "on"
            })
            if self.params["tatm_limit"] is None:
                raise ValueError("Temperature limit (tatm_limit) must be specified for CEA policy!")
        elif policy == "CTax":
            self.params.update({
                "impact": "on",
                "savings": "on",
                "cooperation": "on"
            })
            if self.params["ctax_initial"] <= 0:
                raise ValueError("Initial carbon tax (ctax_initial) must be greater than 0 for CTax policy!")
        elif policy == "Simulation":
            self.params.update({
                "impact": "on",
                "savings": "on",
                "cooperation": "off"
            })

    def compute_burden_share(self):
        burden_share = self.params["burden_share"]
        if burden_share == "equal_per_capita":
            return "Computing burden share based on equal per capita..."
        elif burden_share == "historical_responsability":
            return "Computing burden share based on historical responsibility..."
        else:
            raise ValueError(f"Invalid burden_share: {burden_share}")

    def run(self):
        # Main logic for running the model
        self.configure_params()
        burden_share_result = self.compute_burden_share()
        print("Running climate model with configuration:")
        for key, value in self.params.items():
            print(f"{key}: {value}")
        print(burden_share_result)

# Example usage
if __name__ == "__main__":
    model = ClimateModel()
    model.set_policy("CBudget")
    model.params["cbudget"] = 1000  # Set carbon budget
    model.run()

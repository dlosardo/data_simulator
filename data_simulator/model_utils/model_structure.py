"""
Model Structure class
"""


class ModelStructure(object):
    def __init__(self, model_name, json):
        self.nx = 0
        self.ny = 0
        self.x_variables = []
        self.y_variables = []
        self.x_varcovs = []
        self.y_varcovs = []
        self.x_covs = []
        self.y_covs = []
        self.params = []
        self.json = json
        self.model_type = model_name

    def deserialize_json(self):
        for v in self.json['unconditional_variables']['variables']:
            self.nx = self.nx + 1
            for name, vals in v.items():
                self.x_variables.append(
                    Variable(name=name, mean=float(vals['mean']),
                             variance=float(vals['variance'])))
        for v in self.json['conditional_variables']['variables']:
            self.ny = self.ny + 1
            for name, vals in v.items():
                self.y_variables.append(
                    Variable(name=name, mean=float(vals['mean']),
                             variance=float(vals['variance'])))
        if self.nx > 1:
            for i in range(1, self.nx):
                for j in range(0, i):
                    self.x_covs.append(
                        float(self.json['unconditional_variables'][
                            'covariances'][self.x_variables[j].name][
                                self.x_variables[i].name]))
        if self.ny > 1:
            for i in range(1, self.ny):
                for j in range(0, i):
                    self.y_covs.append(float(self.json[
                        'unconditional_variables']['covariances'][
                            self.y_variables[j].name][
                                self.y_variables[i].name]))

        for i in range(0, len(self.y_variables)):
            for j in range(0, len(self.x_variables)):
                self.params.append(float(
                    self.json['conditional_variables']['structural_relations'][
                        self.y_variables[i].name][self.x_variables[j].name]))

        self.x_varcovs.append(float(self.json[
            'unconditional_variables']['variables'][0][
                self.x_variables[0].name]['variance']))
        for i in range(1, self.nx):
            for j in range(0, i):
                self.x_varcovs.append(float(self.json[
                    'unconditional_variables']['covariances'][
                        self.x_variables[j].name][self.x_variables[i].name]))
            self.x_varcovs.append(float(
                self.json['unconditional_variables']['variables'][
                    i][self.x_variables[i].name]['variance']))

        self.y_varcovs.append(float(self.json[
            'conditional_variables']['variables'][0][
                self.y_variables[0].name]['variance']))
        for i in range(1, self.ny):
            for j in range(0, i):
                self.y_varcovs.append(float(self.json[
                    'conditional_variables']['covariances'][
                        self.y_variables[j].name][self.y_variables[i].name]))
            self.y_varcovs.append(float(
                self.json['conditional_variables']['variables'][
                    i][self.y_variables[i].name]['variance']))

    def get_x_variable_mean_values(self):
        vals = [v.mean for v in self.x_variables]
        return vals

    def get_x_variable_variance_values(self):
        vals = [v.variance for v in self.x_variables]
        return vals

    def get_y_variable_mean_values(self):
        vals = [v.mean for v in self.y_variables]
        return vals

    def get_y_variable_variance_values(self):
        vals = [v.variance for v in self.y_variables]
        return vals


class Variable(object):
    def __init__(self, name, mean, variance):
        self.name = name
        self.mean = mean
        self.variance = variance

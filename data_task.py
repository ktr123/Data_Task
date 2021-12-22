import pandas, re

class Phenom_Data_app:

    def __init__(self,cost,discount):
        self.cost = cost
        self.discount = discount

    def read_data_from_file(self, file_name: str = 'input.txt'):
        """
        :param file_name : Name of the file to read data
        :return:
        """
        final_input_data = []
        data = pandas.read_csv(file_name, index_col=False, header=None)
        for each_data in data.iloc:
            date = re.findall('\d{4}-\d{2}-\d{2}', str(each_data[0]))[0]
            product_size = re.findall(' (\w)', str(each_data[0]))[0]
            product_owner = str(each_data[0]).split(' ')[-1]
            final_input_data.append({'date': date, 'size': product_size, 'shipment_company': product_owner})
        return final_input_data

    def get_smallest_cost_of_product(self, product_size: str,
                          shipment_company: str,
                          total_discount_in_month: int):

        cost = self.cost
        actual_cost_alloted = self.cost[shipment_company][product_size]
        lowest_price_of_product = [cost[each_com][product_size] for each_com in cost]
        lowest_price_of_product.sort()
        discount = actual_cost_alloted - lowest_price_of_product[0]
        if discount < total_discount_in_month:
            return lowest_price_of_product[0], discount, total_discount_in_month
        return actual_cost_alloted, discount, total_discount_in_month

    def add_rules_to_discount(self):
        input_data = self.read_data_from_file()
        discount_data = {}
        for each_data in input_data:
            month_year = ''.join(each_data['date'].split('-'))[0:-2]
            discount_data[month_year] = {'discount': self.discount, 'third_L_shipment': 0} if month_year not in discount_data else discount_data[month_year]
            if each_data['size'] == 'L' and discount_data[month_year]['third_L_shipment'] == 3:
                actual_cost_alloted = self.cost[each_data['shipment_company']]['L']
                cost_allcated = 0
                discount =  actual_cost_alloted
                discount_data[month_year].update({'discount': discount_data[month_year]['discount'] - actual_cost_alloted})
            elif each_data['size'] == 'S':
                cost_allcated, discount, total_discount_in_month = self.get_smallest_cost_of_product(
                    shipment_company=each_data['shipment_company'],
                    total_discount_in_month=discount_data[month_year]['discount'],
                    product_size=each_data['size'])
                discount_data[month_year].update({'discount': total_discount_in_month})
            else:
                cost_allcated = self.cost[each_data['shipment_company']][each_data['size']] if each_data['shipment_company'] in self.cost.keys() else 'Ignored'
                discount_data[month_year]['third_L_shipment'] = discount_data[month_year]['third_L_shipment'] + 1 if each_data['shipment_company'] == 'LP' and each_data['size'] == 'L' else discount_data[month_year]['third_L_shipment']
                discount = 0
            each_data.update({'cost':cost_allcated,'discount':discount})
        return input_data

    def write_data_to_file(self,data):
        df = pandas.DataFrame(data,columns=['date', 'size','shipment_company','cost','discount'])
        df.to_csv('final_output.txt')



cost = {'LP': {'S': 1.5, 'M': 4.9, 'L': 6.9}, 'MR': {'S': 2, 'M': 3, 'L': 4}}
discount =10
obj = Phenom_Data_app(cost,discount)
data = obj.add_rules_to_discount()
obj.write_data_to_file(data)
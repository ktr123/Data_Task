import pandas, re


class Phenom_Data_app:

    def __init__(self, cost, discount):
        self.cost = cost
        self.discount = discount

    def read_data_from_file(self, file_name: str = 'input.txt'):
        final_input_data = []
        data = pandas.read_csv(file_name, index_col=False, header=None)
        for each_data in data.iloc:
            data = re.findall('\S+', str(each_data[0]))
            no_of_words = re.findall('\s+', str(each_data[0]))
            shimpment_company = no_of_words[1] + data[2] if len(no_of_words) == 2 else ''
            final_input_data.append(
                {'date': data[0], 'size': no_of_words[0] + data[1], 'shipment_company': shimpment_company})
        return final_input_data

    def get_smallest_cost_of_product(self, product_size: str,
                                     shipment_company: str,
                                     total_discount_in_month: int):

        cost = self.cost
        actual_cost_alloted = self.cost[shipment_company][product_size]
        lowest_price_of_product = [cost[each_com][product_size] for each_com in cost]
        lowest_price_of_product.sort()
        discount = actual_cost_alloted - lowest_price_of_product[0]
        print(discount, total_discount_in_month)
        if discount < total_discount_in_month:
            return lowest_price_of_product[0], discount, total_discount_in_month
        elif discount > total_discount_in_month:
            return actual_cost_alloted - total_discount_in_month, total_discount_in_month, 0
        return actual_cost_alloted, '-', total_discount_in_month

    def get_data_by_removing_spaces(self, dict_data: dict, dick_key: str):
        return dict_data[dick_key].split(' ')[-1]

    def add_rules_to_discount(self):
        input_data = self.read_data_from_file()
        discount_data = {}
        for each_data in input_data:
            month_year = ''.join(each_data['date'].split('-'))[0:-2]
            discount_data[month_year] = {'discount': self.discount,
                                         'third_L_shipment': 1} if month_year not in discount_data else discount_data[
                month_year]
            size = self.get_data_by_removing_spaces(each_data, 'size')
            company = self.get_data_by_removing_spaces(each_data, 'shipment_company')
            if size == 'L' and company == 'LP' and discount_data[month_year]['third_L_shipment'] == 3 and \
                    self.cost[company]['L'] < discount_data[month_year]['discount']:
                actual_cost_alloted = self.cost[company]['L']
                cost_allcated = 0
                discount = actual_cost_alloted
                discount_data[month_year]['third_L_shipment'] = discount_data[month_year]['third_L_shipment'] + 1
                discount_data[month_year].update(
                    {'discount': discount_data[month_year]['discount'] - actual_cost_alloted})
            elif size == 'S':
                cost_allcated, discount, total_discount_in_month = self.get_smallest_cost_of_product(
                    shipment_company=company,
                    total_discount_in_month=discount_data[month_year]['discount'],
                    product_size=size)
                discount_data[month_year].update(
                    {'discount': total_discount_in_month - discount})
            else:
                cost_allcated = self.cost[company][size] if company in self.cost.keys() else 'Ignored'
                discount_data[month_year]['third_L_shipment'] = discount_data[month_year][
                                                                    'third_L_shipment'] + 1 if company == 'LP' and size == 'L' else \
                    discount_data[month_year]['third_L_shipment']
                discount = '-'

            each_data.update({'cost': cost_allcated, 'discount': discount})
        return input_data

    def write_data_to_file(self, data):
        df = pandas.DataFrame(data, columns=['date', 'size', 'shipment_company', 'cost', 'discount'], )
        print(df)
        df.to_csv('final_output.txt', index=False,)


'''cost = {'LP': {'S': 1.5, 'M': 4.9, 'L': 6.9}, 'MR': {'S': 2, 'M': 3, 'L': 4}}
discount = 10
obj = Phenom_Data_app(cost, discount)
data = obj.add_rules_to_discount()
obj.write_data_to_file(data)'''

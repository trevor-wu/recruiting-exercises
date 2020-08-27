import json
def inventory_allocator(orders, warehouses):
    """
    INPUTS
    orders: dictionary with quantities
    e.g. {'apple': 1, 'banana':1}
    warehouses: list of warehouses (dictionaries with name and inventory)
    e.g. [{'name': 'owd', 'inventory':{'apple': 5,'orange': 10}},{'name': 'dm', 'inventory':{'banana':5,'orange':10}}]
    
    OUTPUTS
    allocation: list of dictionaries with warehouse name and inventory to be delivered from warehouse
    e.g. [{'dm':{'apple':5}}, {'owd':{'apple':5}}]
    """
    warehouse_inventory = {} #{order:{priority:[warehouse, warehouse]}}
    #create warehouse priorities for each order so we can minimize shipping
    for order in orders:
        warehouse_inventory[order] = {}
        for w in warehouses:
            if order in w['inventory']:
                quantity = w['inventory'][order]
                if quantity not in warehouse_inventory[order]:
                    warehouse_inventory[order][quantity] = [w['name']]
                else:
                    warehouse_inventory[order][quantity].append(w['name'])
    order_allocations = {} #{warehouse:{order:quantity, order:quantity}, warehouse}
    #create dictionary which keeps track of where each order will be shipped out of
    for w in warehouses:
        order_allocations[w['name']] = {}
    for order in orders:
        ordered_quantity = orders[order]
        #sort priority
        quantities = [q for q in warehouse_inventory[order]]
        quantities = quantities[::-1]
        quantities.sort()
        #go down by warehouse priority
        for q in quantities:
            warehouses_of_same_priority = warehouse_inventory[order][q]
            for warehouse in warehouses_of_same_priority:
                allocation = min(q, ordered_quantity)
                if allocation > 0:
                    order_allocations[warehouse][order] = allocation
                ordered_quantity = max(ordered_quantity - q, 0) #partially fulfilled
        if ordered_quantity > 0: #not fulfilled
            #order not possible
            return []
    #clean it up
    allocations = []
    for w in order_allocations:
        if len(order_allocations[w]) > 0:
            allocations.append({w:order_allocations[w]})
    return allocations

test_file = open('tests.json',)
tests = json.load(test_file)
for test in tests:
    print("===NEW=TEST===================")
    print("ORDERS")
    orders = test['orders']
    warehouses = test['warehouses']
    for order in orders:
        print(order + " : " + str(orders[order]))
    print("------------------------------")
    print("WAREHOUSES")
    for w in warehouses:
        print(w)
    result = inventory_allocator(orders, warehouses)
    print("------------------------------")
    print("ALLOCATION")
    if result == []:
        print('Order cannot be fulfilled! Not enough inventory!')
    else:
        for r in result:
            print(r)
            
    
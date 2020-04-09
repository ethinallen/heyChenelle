import pandas as pd
import random
import numpy as np
import re

class handler():

    sincereApology =    '''
                            Hey Franz,
                                    I wrote these methods before I found out about the `.groupby`
                                    function. I didn't particularly want to rewrite these functions
                                    because they work they just take long because I did them
                                    iteratively. Thanks for your consideration in this matter and I
                                    hope to have the answer to you shortly.

                            Best,
                            Drew

                        '''

    dfdict = {
        'regions'       : pd.read_csv('AirportRegions.csv'),
        'demand'       : pd.read_csv('PaxDemand.csv'),
        'demandDist'    : pd.read_csv('PaxDemandDist.csv'),
        'pricesDF'      : pd.read_csv('TicketPrices.csv'),
        'zipRegions'    : pd.read_csv('Zip2Regions.csv')
    }

    airportCount = {}
    zipCount = {}

    # describe the dataframs in dfdict
    def describe(self):
        for key in self.dfdict:
            print(self.dfdict[key].describe())

    '''
        Method for Question 1
    '''
    def airportsInRegions(self):
        for i, row in self.dfdict['regions'].iterrows():
            region = row['Region']
            if region in self.airportCount:
                self.airportCount[region] += 1
            else:
                self.airportCount[region] = 1
        print(self.airportCount)

    '''
        Method for Question 2
    '''
    def regionWithMostZipvalues(self):
        for i, row in self.dfdict['zipRegions'].iterrows():
            region = row['Region']
            if region in self.zipCount:
                self.zipCount[region] += 1
            else:
                self.zipCount[region] = 1
        print(self.zipCount)

    '''
        Method for task 3
    '''
    def revenuePerAirport(self):

        print(self.sincereApology)

        counts = {}

        pDF = self.dfdict['pricesDF']
        pDF = pDF.replace(',', '', regex=True)
        fDF = self.dfdict['demand']

        for index, row in self.dfdict['demandDist'].iterrows():
            forecastDF = fDF
            forecastDF = forecastDF.loc[forecastDF['Zip2'] == row['OrigZip2']]
            forecast = forecastDF['WeeklyTicketFC'].item()
            if row['DestAirport'] not in counts:
                counts[row['DestAirport']] = {  'volume'    : 0,
                                                'revenue'   : 0
                                                }
                addition = (row['FirstClass'] + row['BusinessClass'] + row['MainCabin'] + row['Economy'])
            else:
                addition = row['FirstClass'] + row['BusinessClass'] + row['MainCabin'] + row['Economy']


            counts[row['DestAirport']]['volume'] += (addition * forecast)
            priceDF = pDF
            priceDF = priceDF.loc[priceDF['DestAirport'] == row['DestAirport']]
            priceDF = priceDF.loc[priceDF['OrigZip2'] == row['OrigZip2']]
            priceDF['FirstClass'] = priceDF['FirstClass'].astype(float)
            priceDF['BusinessClass'] = priceDF['BusinessClass'].astype(float)
            priceDF['MainCabin'] = priceDF['MainCabin'].astype(float)
            priceDF['Economy'] = priceDF['Economy'].astype(float)

            revenue = 0
            revenue +=  row['FirstClass'] * priceDF['FirstClass'].item() * forecast
            revenue +=  row['BusinessClass'] * float(priceDF['BusinessClass'].item()) * forecast
            revenue +=  row['MainCabin'] * float(priceDF['MainCabin'].item()) * forecast
            revenue +=  row['Economy'] * float(priceDF['Economy'].item()) * forecast
            counts[row['DestAirport']]['revenue'] += revenue

        countsForCSV = {'destAirport'   : [],
                        'WeeklyArrivals'        : [],
                        'revenue'       : []
                        }

        for airport in counts:
            countsForCSV['destAirport'].append(airport)
            countsForCSV['WeeklyArrivals'].append(counts[airport]['volume'] * .01)
            countsForCSV['revenue'].append(counts[airport]['revenue'])

        df = pd.DataFrame.from_dict(countsForCSV)
        df.to_csv('question3.csv', sep=',', encoding='utf-8')
        print('Wrote question3.csv')

    '''
        Method for Question 4
    '''
    def revenuePerRegion(self):

        print(self.sincereApology)

        counts = {}

        priceDF = self.dfdict['pricesDF']
        priceDF = priceDF.replace(',', '', regex=True)

        for index, row in self.dfdict['demandDist'].iterrows():

            forecastDF = self.dfdict['demand']
            forecastDF = forecastDF.loc[forecastDF['Zip2'] == row['OrigZip2']]
            forecast = forecastDF['WeeklyTicketFC'].item()


            if row['OrigZip2'] not in counts:
                counts[row['OrigZip2']] = {  'volume'    : 0,
                                                'revenue'   : 0}
                addition = row['FirstClass'] + row['BusinessClass'] + row['MainCabin'] + row['Economy']
            else:
                addition = row['FirstClass'] + row['BusinessClass'] + row['MainCabin'] + row['Economy']


            counts[row['OrigZip2']]['volume'] += addition

            tempPriceDF = priceDF
            tempPriceDF = tempPriceDF.loc[tempPriceDF['DestAirport'] == row['DestAirport']]
            tempPriceDF = tempPriceDF.loc[tempPriceDF['OrigZip2'] == row['OrigZip2']]
            tempPriceDF['FirstClass'] = tempPriceDF['FirstClass'].astype(float)
            tempPriceDF['BusinessClass'] = tempPriceDF['BusinessClass'].astype(float)
            tempPriceDF['MainCabin'] = tempPriceDF['MainCabin'].astype(float)
            tempPriceDF['Economy'] = tempPriceDF['Economy'].astype(float)

            revenue = 0
            revenue +=  row['FirstClass'] * tempPriceDF['FirstClass'].item() * forecast
            revenue +=  row['BusinessClass'] * float(tempPriceDF['BusinessClass'].item()) * forecast
            revenue +=  row['MainCabin'] * float(tempPriceDF['MainCabin'].item()) * forecast
            revenue +=  row['Economy'] * float(tempPriceDF['Economy'].item()) * forecast
            counts[row['OrigZip2']]['revenue'] += revenue

        countsForCSV = {
                        'region'        : [],
                        'counts'        : [],
                        'revenue'       : []
                        }

        for region in counts:
            countsForCSV['region'].append(region)
            countsForCSV['counts'].append(counts[region]['volume'] * .01)
            countsForCSV['revenue'].append(counts[region]['revenue'])

        df = pd.DataFrame.from_dict(countsForCSV)
        df.to_csv('question4.csv', sep=',', encoding='utf-8')
        print('Wrote question4.csv')


    '''
        Method for Question 5
    '''
    def randomRemove(self):
        zipToRemoveFrom = int(input("Enter a Zip2 to have an aiport removed from:\t"))
        zipDF = self.dfdict['demandDist']
        zipDF = zipDF.loc[zipDF['OrigZip2'] == zipToRemoveFrom]
        length = zipDF.shape[0]
        removalIndex = random.randint(0, length - 1)
        zipDF = zipDF.drop(zipDF.index[removalIndex])
        zipDF = zipDF[['FirstClass', 'BusinessClass', 'MainCabin', 'Economy']]
        zipArr = zipDF.values
        arrSum = np.sum(zipArr)
        for i, row in enumerate(zipArr):
            for j, val in enumerate(row):
                zipArr[i][j] = zipArr[i][j] / arrSum * 100
        zipDF = self.dfdict['demandDist'][['FirstClass', 'BusinessClass', 'MainCabin', 'Economy']]
        zipDF.drop(zipDF.index[removalIndex])
        cleansedDF = pd.DataFrame({'FirstClass': zipArr[:, 0],'BusinessClass': zipArr[:, 1],'MainCabin': zipArr[:, 2],'Economy': zipArr[:, 3]})
        result = pd.concat([zipDF, cleansedDF], axis=1, join='inner')
        print(result)


    '''
        Method for question 6
    '''
    def actualPassengerDemand(self):
        df = self.dfdict['demand']

        def makeDist(row):
            mean = row['WeeklyTicketFC'].item()
            low = mean * .9
            high = mean * 1.1
            arr = np.random.uniform(low, high, 100)
            return arr

        def makeMean(row):
            mean = np.mean(row['arr'])
            return mean

        def makeDev(row):
            stdDev = np.std(row['arr'])
            return stdDev

        def makeCI(row):
            lower = row['mean'] - 2 * row['dev']
            upper = row['mean'] + 2 * row['dev']
            stringCI = str(lower) + ' - ' + str(upper)
            return stringCI

        df['arr'] = df.apply (lambda row: makeDist(row), axis=1)
        df['mean'] = df.apply (lambda row: makeMean(row), axis=1)
        df['dev'] = df.apply (lambda row: makeDev(row), axis=1)
        df['confidenceInterval'] = df.apply (lambda row: makeCI(row), axis=1)

        df = df.drop('arr', 1)
        df.to_csv('question6.csv')
        print('Wrote to question6.csv')

    '''
        Method for question 7
    '''
    def meanValuePerClass(self):
        df = self.dfdict['demandDist']
        sorted = df.groupby('OrigZip2').groups

        values = {}
        for zip in sorted:
            values[zip] = {
                            'first'     : [],
                            'business'  : [],
                            'main'      : [],
                            'econ'      : []
                          }
            indexes = sorted[zip]
            for num, index in enumerate(indexes):
                row = df.loc[index]
                values[zip]['first'].append(row['FirstClass'].item())
                values[zip]['business'].append(row['BusinessClass'].item())
                values[zip]['main'].append(row['MainCabin'].item())
                values[zip]['econ'].append(row['Economy'].item())

        zipAvgs = pd.DataFrame(columns=['OrigZip2', 'First Class', 'Business Class', 'Main Cabin', 'Economy'])

        for zip in values:
            row = {     'OrigZip2'          : zip,
                        'FirstClass'       : np.mean(values[zip]['first']),
                        'Business Class'    : np.mean(values[zip]['business']),
                        'MainCabin'        : np.mean(values[zip]['main']),
                        'Economy'           : np.mean(values[zip]['econ'])
                }

            zipAvgs = zipAvgs.append(row, ignore_index=True)
        zipAvgs.to_csv('question7.csv')
        print('Wrote to question7.csv')

    '''
        Method for question 8
    '''
    def csvByQuarter(self):
        df = self.dfdict['pricesDF']
        df = df.replace(',', '', regex=True)

        def getMonth(row):
            splitDate = row['Date'].split('/')
            month = splitDate[0]
            return month

        df['month'] = df.apply (lambda row: getMonth(row), axis=1)

        classes = {
                    'first'     : {
                                    'first' : [],
                                    'second': [],
                                    'third' : [],
                                    'fourth': []
                                    },
                    'business'  : {
                                    'first' : [],
                                    'second': [],
                                    'third' : [],
                                    'fourth': []
                                    },
                    'main'      : {
                                    'first' : [],
                                    'second': [],
                                    'third' : [],
                                    'fourth': []
                                    },
                    'econ'      : {
                                    'first' : [],
                                    'second': [],
                                    'third' : [],
                                    'fourth': []
                                    }
                    }

        for index, row in df.iterrows():
            if int(row['month']) / 3 <= 1:
                classes['first']['first'].append(float(row['FirstClass']))
                classes['business']['first'].append(int(row['BusinessClass']))
                classes['main']['first'].append(int(row['MainCabin']))
                classes['econ']['first'].append(int(row['Economy']))
            elif int(row['month']) / 3 <= 2:
                classes['first']['second'].append(float(row['FirstClass']))
                classes['business']['second'].append(int(row['BusinessClass']))
                classes['main']['second'].append(int(row['MainCabin']))
                classes['econ']['second'].append(int(row['Economy']))
            elif int(row['month']) / 3 <= 3:
                classes['first']['third'].append(float(row['FirstClass']))
                classes['business']['third'].append(int(row['BusinessClass']))
                classes['main']['third'].append(int(row['MainCabin']))
                classes['econ']['third'].append(int(row['Economy']))
            else:
                classes['first']['fourth'].append(float(row['FirstClass']))
                classes['business']['fourth'].append(int(row['BusinessClass']))
                classes['main']['fourth'].append(int(row['MainCabin']))
                classes['econ']['fourth'].append(int(row['Economy']))


        quarters = pd.DataFrame(columns=['Fare', 'Q1', 'Q2', 'Q3', 'Q4'])

        for c in classes:
            result =    {
                            'Fare'  : c,
                            'Q1'    : np.mean(classes[c]['first']),
                            'Q2'    : np.mean(classes[c]['second']),
                            'Q3'    : np.mean(classes[c]['third']),
                            'Q4'    : np.mean(classes[c]['fourth'])
                        }

            quarters = quarters.append(result, ignore_index=True)

        quarters.to_csv('question8.csv')
        print('Wrote to question8.csv')

    '''
        new method for problem 3
    '''
    # def newRevenuePerAirport(self):


if __name__ == '__main__':
    h = handler()
    # h.airportsInRegions()
    # h.regionWithMostZipvalues()
    # h.revenuePerAirport()
    # h.revenuePerRegion()
    # h.randomRemove()
    h.actualPassengerDemand()
    # h.meanValuePerClass()
    # h.csvByQuarter()

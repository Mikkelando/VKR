import matplotlib.pyplot as plt

def plot_results(results, config):
    """
    Визуализация результатов: инвестиции, интенсивность выбросов, температура.
    """
    t_sequence = config['t_sequence']

    investments = [results[t]['investment'] for t in t_sequence]
    emissions_intensities = [results[t]['emissions_intensity'] for t in t_sequence]
    temperatures = [results[t]['objective_value'] for t in t_sequence]

    # График инвестиций
    plt.figure()
    plt.plot(t_sequence, investments, label='Investment')
    plt.xlabel('Time')
    plt.ylabel('Investment')
    plt.title('Investment over time')
    plt.legend()
    plt.savefig(f"{config['results_path']}/investment.png")

    # График интенсивности выбросов
    plt.figure()
    plt.plot(t_sequence, emissions_intensities, label='Emissions Intensity')
    plt.xlabel('Time')
    plt.ylabel('Emissions Intensity')
    plt.title('Emissions Intensity over time')
    plt.legend()
    plt.savefig(f"{config['results_path']}/emissions_intensity.png")

    # График температуры
    plt.figure()
    plt.plot(t_sequence, temperatures, label='Temperature Change')
    plt.xlabel('Time')
    plt.ylabel('Temperature Change')
    plt.title('Temperature Change over time')
    plt.legend()
    plt.savefig(f"{config['results_path']}/temperature_change.png")


def generate_reports(results, config):
    """
    Создание итогового отчёта.
    """
    t_sequence = config['t_sequence']
    welfare = [results[t]['welfare'] for t in t_sequence]
    damages = [results[t]['damages'] for t in t_sequence]
    temperature = [results[t]['temperature'] for t in t_sequence]

    print("Итоговая полезность по годам:", welfare)
    print("Ущерб по годам:", damages)
    print("Температура по годам:", temperature)

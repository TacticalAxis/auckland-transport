import {
    Client,
    IntentsBitField,
    Message,
    REST,
    Routes,
    SlashCommandBuilder,
    EmbedBuilder
} from 'discord.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

type ClassifiedVehicles = {
    boats: string[];
    buses: string[];
    trains: string[];
};

type SingleBus = {
    position: Position,
    attributes: Attributes
}

type Position = {
    latitude: Number,
    longitude: Number,
    speed: Number,
    bearing: string
}

type Attributes = {
    id: string,
    label: string,
    licencePlate: string,
    tripId: string,
    startTime: string,
    startDate: string,
    routeId: string,
    occupancyStatus: 1
}

function classifyVehicles(vehicleList: string[]): ClassifiedVehicles {
    // Initialize the dictionary with empty arrays
    const result: ClassifiedVehicles = {
        boats: [],
        buses: [],
        trains: [],
    };

    // Define regular expressions for buses and trains
    const busRegex = /^[A-Z]{2}\d{3,4}$/;  // Example: AB123, AB1234
    const trainRegex = /^[A-Z]{3}\d{3}$/;  // Example: ABC123

    // Filter and classify the vehicles
    vehicleList
        .filter(item => item && item.trim() !== "") // Remove null/empty strings
        .forEach(vehicle => {
            const normalizedVehicle = vehicle.trim(); // Remove any leading/trailing whitespace

            if (busRegex.test(normalizedVehicle)) {
                result.buses.push(normalizedVehicle);
            } else if (trainRegex.test(normalizedVehicle)) {
                result.trains.push(normalizedVehicle);
            } else {
                result.boats.push(normalizedVehicle); // Default to boat if not bus or train
            }
        });

    return result;
}

// Initialize Discord client with the necessary intents
const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent
    ]
});

// Slash command registration setup
const commands = [
    new SlashCommandBuilder()
        .setName('bus')
        .setDescription('Find a bus by its ID')
        .addStringOption((option) =>
            option
                .setName('busid')
                .setDescription('The ID of the bus')
                .setRequired(true)
        )
].map((command) => command.toJSON());

const rest = new REST({ version: '10' }).setToken(process.env.BOT_TOKEN!);

// Function to fetch data from example.com
async function fetchExample(): Promise<BusData> {
    try {
        const response = await axios.get('http://localhost:8080/v1/auckland-transport/getLocalBuses');
        return response.data;  // Return the response data
    } catch (error) {
        console.error('Error fetching data:', error);
        throw new Error('Failed to fetch data');
    }
}

// Function to fetch data from example.com
async function fetchExample2(busId: string): Promise<SingleBus> {
    try {
        const response = await axios.get(`http://localhost:8080/v1/auckland-transport/getBusData?busId=${busId}`);
        return response.data;  // Return the response data
    } catch (error) {
        console.error('Error fetching data:', error);
        throw new Error('Failed to fetch data');
    }
}

// Function to create an embed from the bus dictionary
function generateListEmbed(title: string, description: string, busDict: Record<string, string>): EmbedBuilder {
    const embed = new EmbedBuilder()
        .setColor(0x0099FF)
        .setTitle(title)
        .setDescription(description)
        .setTimestamp();

    // Add the bus ID entries to the embed
    for (const [key, value] of Object.entries(busDict)) {
        embed.addFields({ name: key, value: value, inline: true });
    }

    embed.setFooter({ text: 'Some footer text here', iconURL: 'https://i.imgur.com/AfFp7pu.png' });
    return embed;
}

client.once('ready', async () => {
    console.log(`${client?.user?.username} Bot is ONLINE`);

    try {
        console.log('Refreshing slash commands...');
        await rest.put(Routes.applicationCommands(client.user!.id), {
            body: commands
        });
        console.log('Slash commands registered!');
    } catch (error) {
        console.error('Error registering slash commands:', error);
    }
});

function processBusIds(busIds: string[]): Record<string, string> {
    // Dictionary to store the result
    const busDict: Record<string, string> = {};

    // Regular expression to match the required pattern
    const regex = /^[A-Za-z]{2}\d{3,4}$/; // Two letters followed by 3 or 4 numbers

    // Filter, sort, and process bus IDs
    const validBusIds = busIds.filter(id => regex.test(id)).sort();

    // Populate the dictionary
    validBusIds.forEach(id => {
        const key = id.substring(0, 2); // First two letters as key
        // If the key already exists, concatenate the new ID
        if (busDict[key]) {
            busDict[key] += `, ${id}`;
        } else {
            // If not, create a new entry in the dictionary
            busDict[key] = id;
        }
    });

    return busDict;
}

// Define a type for the bus data
type BusData = string[]; // Assuming the data is an array of strings

// Listen for slash command interactions
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) return;

    const { commandName, options } = interaction;


    if (commandName === 'listbus') {
        try {
            const data: BusData = await fetchExample();
            const busDict = processBusIds(data); // Expecting data to be a string array

            // Create an embed with the processed bus data
            const exampleEmbed = generateListEmbed(`Bus Information for Auckland Transport Vehicles`, 'Here is the information:', busDict);

            await interaction.reply({ embeds: [exampleEmbed] }); // Reply with the embed
        } catch (error) {
            console.error('Error:', error);
            await interaction.reply('Failed to fetch bus data!');
        }
    }

    if (commandName === 'bus') {
        try {
            // bus Id
            const busId = options.get("busid")?.value;



            console.log("Options: " + JSON.stringify(options.get("busid")?.value, null, 2))

            // Fetch data for the specific bus ID

            console.log("Classified: " + JSON.stringify(classifyVehicles(data), null, 2))

            // Process the fetched data into a dictionary
            const busDict = processBusIds(data); // Expecting data to be a string array

            // Create an embed with the processed bus data
            const exampleEmbed = generateListEmbed(`Bus Information for Auckland Transport Vehicles`, 'Here is the information:', busDict);

            await interaction.reply({ embeds: [exampleEmbed] }); // Reply with the embed
        } catch (error) {
            console.error('Error:', error);
            await interaction.reply('Failed to fetch bus data!');
        }
    }
});

client.login(process.env.BOT_TOKEN);

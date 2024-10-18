import {
    Client,
    IntentsBitField,
    Message,
    REST,
    Routes,
    SlashCommandBuilder
} from 'discord.js';
import dotenv from 'dotenv';

dotenv.config();

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

// Listen for slash command interactions
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) return;

    const { commandName, options } = interaction;

    if (commandName === 'bus') {
        // const busId = options.data.('busid');
        // console.log("Optionss: " + interaction.options.get('busid').)
        // const reason = interaction.options.getString('reason') ?? 'No reason provided';
        const busId = "2";
        console.log(`FOUND BUS ${busId}`);
        await interaction.reply(`FOUND BUS ${busId}`);
    }
});

client.login(process.env.BOT_TOKEN);

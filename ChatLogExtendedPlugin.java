package net.runelite.client.plugins.ChatLogExtended;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.encoder.PatternLayoutEncoder;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.rolling.RollingFileAppender;
import ch.qos.logback.core.rolling.TimeBasedRollingPolicy;
import com.google.inject.Inject;
import com.google.inject.Provides;
import net.runelite.api.events.ChatMessage;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import org.slf4j.LoggerFactory;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@PluginDescriptor(name = "Chat Log Extended", description = "Logs chat messages to a file")
public class ChatLogExtendedPlugin extends Plugin {

    private static final String BASE_DIRECTORY = System.getProperty("user.home") + "/.runelite/chatlogs/";

    @Inject
    private ChatLogExtendedConfig config;

    private Logger publicChatLogger;
    private Logger privateChatLogger;
    private Logger clanChatLogger;

    @Provides
    ChatLogExtendedConfig provideConfig(ConfigManager configManager) {
        return configManager.getConfig(ChatLogExtendedConfig.class);
    }

    @Override
    protected void startUp() {
        publicChatLogger = setupLogger("PublicChatLogger", "public");
        privateChatLogger = setupLogger("PrivateChatLogger", "private");
        clanChatLogger = setupLogger("ClanChatLogger", "clan");
    }

    @Subscribe
    public void onChatMessage(ChatMessage event) {
        switch (event.getType()) {

            case CLAN_MESSAGE:
                if (config.logClanChat()) {
                    clanChatLogger.info("{}", event.getMessage());
                }

	    case CLAN_CHAT:
                if (config.logClanChat()) {
                    clanChatLogger.info("[{}] {}: {}", event.getSender(), event.getName(), event.getMessage());
                }
                break;

            case PRIVATECHAT:
            case MODPRIVATECHAT:
                if (config.logPrivateChat()) {
                    privateChatLogger.info("{}: {}", event.getName(), event.getMessage());
                }
                break;
            case MODCHAT:
            case PUBLICCHAT:
                if (config.logPublicChat()) {
                    publicChatLogger.info("{}: {}", event.getName(), event.getMessage());
                }
                break;
        }
    }

    private Logger setupLogger(String loggerName, String subFolder) {
        LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();

        PatternLayoutEncoder encoder = new PatternLayoutEncoder();
        encoder.setContext(context);
        encoder.setPattern("%d{HH:mm:ss} %msg%n");
        encoder.start();

        String directory = BASE_DIRECTORY + subFolder + "/";

        RollingFileAppender<ILoggingEvent> appender = new RollingFileAppender<>();
        appender.setFile(directory + "latest.log");
        appender.setAppend(true);
        appender.setEncoder(encoder);
        appender.setContext(context);

        TimeBasedRollingPolicy<ILoggingEvent> logFilePolicy = new TimeBasedRollingPolicy<>();
        logFilePolicy.setContext(context);
        logFilePolicy.setParent(appender);
        logFilePolicy.setFileNamePattern(directory + "chatlog_%d{yyyy-MM-dd}.log");
        logFilePolicy.setMaxHistory(30);
        logFilePolicy.start();

        appender.setRollingPolicy(logFilePolicy);
        appender.start();

        Logger logger = context.getLogger(loggerName);
        logger.detachAndStopAllAppenders();
        logger.setAdditive(false);
        logger.setLevel(Level.INFO);
        logger.addAppender(appender);

        return logger;
    }
}

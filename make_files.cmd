$root = "PerceptionNodeSuit"
$structure = @(
    "SocialMediaPlatform\OAuthClient\AccessTokenManagement",
    "SocialMediaPlatform\OAuthClient\RateLimitHandling",
    "SocialMediaPlatform\ContentManagement\Post\CreatePost",
    "SocialMediaPlatform\ContentManagement\Post\DeletePost",
    "SocialMediaPlatform\ContentManagement\Media\UploadMedia",
    "SocialMediaPlatform\ContentManagement\Media\DeleteMedia",
    "SocialMediaPlatform\ContentManagement\Comment\CreateComment",
    "SocialMediaPlatform\ContentManagement\Comment\DeleteComment",
    "SocialMediaPlatform\UserManagement\UserInfo",
    "SocialMediaPlatform\UserManagement\UserActivity",
    "SocialMediaPlatform\Analytics\EngagementMetrics",
    "SocialMediaPlatform\Analytics\AudienceInsights",
    "PlatformSpecificFeatures\TwitterFeatures\TweetStream",
    "PlatformSpecificFeatures\TwitterFeatures\FollowUnfollow",
    "PlatformSpecificFeatures\InstagramFeatures\StoryUpload",
    "PlatformSpecificFeatures\InstagramFeatures\IGTV",
    "PlatformSpecificFeatures\LinkedInFeatures\JobPosting",
    "PlatformSpecificFeatures\LinkedInFeatures\CompanyUpdates",
    "PlatformSpecificFeatures\RedditFeatures\SubredditManagement",
    "PlatformSpecificFeatures\RedditFeatures\KarmaPoints",
    "PlatformSpecificFeatures\TikTokFeatures\VideoEffects",
    "PlatformSpecificFeatures\TikTokFeatures\MusicLibrary",
    "PlatformSpecificFeatures\YouTubeFeatures\VideoAnalytics",
    "PlatformSpecificFeatures\YouTubeFeatures\LiveStreaming",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryManagement\CreateRepository",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryManagement\CloneRepository",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryManagement\DeleteRepository",
    "PlatformSpecificFeatures\GitHubFeatures\IssueTracking\CreateIssue",
    "PlatformSpecificFeatures\GitHubFeatures\IssueTracking\CommentOnIssue",
    "PlatformSpecificFeatures\GitHubFeatures\IssueTracking\CloseIssue",
    "PlatformSpecificFeatures\GitHubFeatures\CodeCollaboration\PullRequest",
    "PlatformSpecificFeatures\GitHubFeatures\CodeCollaboration\CodeReview",
    "PlatformSpecificFeatures\GitHubFeatures\CodeCollaboration\MergeCode",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryWatch\SubscribeToRepo",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryWatch\UnsubscribeFromRepo",
    "PlatformSpecificFeatures\GitHubFeatures\RepositoryWatch\ListSubscribers"
)

foreach ($path in $structure) {
    $dirs = $path -split '\\'
    $fileName = $dirs[-1] + ".py"
    $dirPath = $root + "\" + ($dirs[0..($dirs.Count - 2)] -join "\")

    if (-not (Test-Path -Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force
    }

    $filePath = Join-Path -Path $dirPath -ChildPath $fileName
    New-Item -ItemType File -Path $filePath -Force
}
